import os
import time

from flask import Flask, request, jsonify
import requests as http_requests

app = Flask(__name__)

# In-memory key-value store
store = {}

# Configuration from environment
NODE_NAME = os.environ.get("NODE_NAME", "node1")
PEERS = [p for p in os.environ.get("PEERS", "").split(",") if p]
MODE = os.environ.get("MODE", "CP")


@app.route("/data", methods=["GET"])
def get_all_data():
    return jsonify({"node": NODE_NAME, "mode": MODE, "store": store})


@app.route("/data/<key>", methods=["GET"])
def get_data(key):
    if key in store:
        return jsonify({"node": NODE_NAME, "key": key, "value": store[key]})
    return jsonify({"error": "Key not found"}), 404


@app.route("/data/<key>", methods=["PUT"])
def put_data(key):
    global MODE
    value = request.json.get("value")

    if MODE == "CP":
        # CP Mode: Replicate to ALL peers before confirming
        for peer in PEERS:
            try:
                resp = http_requests.post(
                    f"http://{peer}/replicate",
                    json={"key": key, "value": value},
                    timeout=2,
                )
                if resp.status_code != 200:
                    return jsonify({
                        "error": f"Replication to {peer} failed",
                        "reason": "Write rejected to maintain consistency (CP mode)",
                    }), 503
            except http_requests.exceptions.RequestException:
                return jsonify({
                    "error": f"Cannot reach {peer}",
                    "reason": "Write rejected to maintain consistency (CP mode)",
                }), 503

        # All peers confirmed, write locally
        store[key] = value
        return jsonify({
            "status": "ok",
            "node": NODE_NAME,
            "key": key,
            "value": value,
            "mode": "CP",
            "message": "All nodes consistent",
        })

    else:
        # AP Mode: Write locally first, replicate best-effort
        store[key] = value

        replication_results = []
        for peer in PEERS:
            try:
                http_requests.post(
                    f"http://{peer}/replicate",
                    json={"key": key, "value": value},
                    timeout=1,
                )
                replication_results.append({"peer": peer, "status": "replicated"})
            except http_requests.exceptions.RequestException:
                replication_results.append({"peer": peer, "status": "unreachable"})

        return jsonify({
            "status": "ok",
            "node": NODE_NAME,
            "key": key,
            "value": value,
            "mode": "AP",
            "replication": replication_results,
        })