# ⚡ Distributed Key-Value Store | Exploring the CAP Theorem

A small, containerized distributed system built to explore one of the most fundamental trade-offs in distributed systems: **Consistency vs. Availability during network partitions.**

Built with Python, Flask, and Docker Compose, this project runs three independent nodes that replicate key-value data over HTTP.

Credits - [NextWorkAI](https://nextwork.ai/projects/56330f0f-e0c6-474e-bda9-d625ff412ba0)

## 🧠 What I Explored

The [CAP theorem](https://en.wikipedia.org/wiki/CAP_theorem) states that when a network partition occurs, a distributed system cannot guarantee both consistency and availability for every request.

This project demonstrates two approaches:

| | **CP Mode** | **AP Mode** |
|---|---|---|
| Primary goal | Consistency | Availability |
| Write strategy | Replicate before acknowledging | Write locally, replicate best-effort |
| When a peer is unreachable | Reject the write | Accept the write |
| Data behavior | Partial replication is possible in this implementation | Replicas may temporarily diverge |
| Recovery | Manual synchronization | Manual synchronization |

> **Key takeaway:** Distributed systems aren't just about replicating data. They're about deciding what happens when replication fails.

## 🏗️ Architecture

```text
                 Client
                    |
          +---------+---------+
          |         |         |
       Node 1    Node 2    Node 3
       :5001     :5002     :5003
          |         |         |
          +---- HTTP Replication ----+
                    |
             Docker Network
```

Each node runs the same Flask application in its own Docker container, with an independent in-memory key-value store.

Nodes discover one another through Docker Compose service names and communicate using HTTP endpoints.

## ✨ Features

- **Three-node architecture** — independent nodes running in Docker containers.
- **CP and AP modes** — switch replication behavior at runtime.
- **HTTP-based replication** — propagate key-value updates between peers.
- **Timestamp-based conflict resolution** — use Last-Write-Wins (LWW) when merging updates.
- **Manual synchronization** — reconcile newer entries from reachable peers.
- **Failure simulation** — stop a node and observe how writes behave.
- **REST API** — create, retrieve, and inspect stored values.

## 🛠️ Tech Stack

`Python` · `Flask` · `Docker` · `Docker Compose` · `REST APIs` · `Distributed Systems`

## 🚀 Getting Started

### Prerequisites

- Docker
- Docker Compose

### Run the nodes

```bash
docker compose up --build
```

The nodes are available at:

| Node | Endpoint |
|---|---|
| Node 1 | `http://localhost:5001` |
| Node 2 | `http://localhost:5002` |
| Node 3 | `http://localhost:5003` |

### Write a value

```bash
curl.exe -X PUT http://localhost:5001/data/color \
  -H "Content-Type: application/json" \
  -d "{\"value\":\"blue\"}"
```

### Read a value

```bash
curl.exe http://localhost:5001/data/color
```

### Switch to AP mode

Send a `POST` request to `/mode` with this JSON body:

```json
{
  "mode": "AP"
}
```

Example endpoint: `http://localhost:5001/mode`

Each node's mode is configured independently.

## 🧪 Try It Yourself

1. Start all three nodes.
2. Write a value through Node 1.
3. Stop Node 3 using `docker stop node3`.
4. Attempt another write in CP mode.
5. Switch the nodes to AP mode and repeat.
6. Restart Node 3 and experiment with the `/sync` endpoint.

Observe how the write response and the contents of each node's local store differ.

## ⚠️ Limitations

- CP writes can leave partial updates on replicas when a later replication request fails.
- AP replicas can diverge during network failures.
- Synchronization is manual and does not handle deletions.
- Timestamp-based LWW can be affected by clock differences and concurrent writes.
- Data is in memory and is lost when a container restarts.
- Consensus, durable storage, and automatic recovery are not implemented.

## 🎯 What This Project Taught Me

- How replication works across independent service instances.
- Why network partitions complicate consistency and availability.
- Why partial writes occur and why rollback is not trivial.
- How timestamp-based conflict resolution works—and where it falls short.
- Why real distributed databases need stronger coordination and recovery mechanisms.

---

*Built as a hands-on exploration of distributed systems, fault tolerance, and the CAP theorem.*
