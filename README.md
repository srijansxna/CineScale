# CineScale

The Latest updates are on the dev branch of the repo. please check it for the work done.....




A Distributed Video Processing & Streaming Pipeline

📌 Overview

CineScale is a backend-heavy, cloud-native system inspired by Netflix’s internal video pipeline.
It demonstrates how large video platforms ingest raw media, process it into multiple formats, and serve it efficiently at scale using Python, Docker, Kubernetes, FFmpeg, and async workers.

This project focuses on systems design, scalability, containerization, and distributed processing rather than UI.

🧠 What Problem Does CineScale Solve?

Uploading a video is easy.
Processing, encoding, storing, and streaming it reliably at scale is hard.

CineScale simulates:

High-load video ingestion

Asynchronous video processing

Multiple resolution outputs

Scalable deployment using containers and orchestration

🏗️ System Architecture
Client
  ↓
FastAPI (Upload & Metadata Service)
  ↓
Message Queue (Redis / RabbitMQ)
  ↓
Worker Nodes (FFmpeg Processing)
  ↓
Object Storage (Local / S3)
  ↓
Streaming API

Core Principles Used

Microservices

Async task queues

Stateless APIs

Horizontal scalability

Fault isolation

⚙️ Tech Stack
Backend

Python 3.10+

FastAPI – REST APIs

FFmpeg – Video transcoding

Distributed Processing

Celery – Background workers

Redis / RabbitMQ – Message broker

Storage

Local filesystem (development)

S3-compatible storage (optional extension)

DevOps & Infra

Docker – Containerization

Docker Compose – Local orchestration

Kubernetes – Production-grade orchestration

Nginx – Reverse proxy & streaming

✨ Features
📤 Video Upload

Upload raw video files

Metadata stored separately

Non-blocking request handling

🔄 Asynchronous Processing

Videos are transcoded in background

Generates multiple resolutions:

240p

360p

720p

📡 Streaming Support

Resolution-based streaming endpoints

HTTP-based delivery

📈 Scalability

Multiple worker replicas

Queue-based load balancing

Kubernetes-ready deployment

📂 Project Structure
cinescale/
│
├── api/
│   ├── main.py
│   ├── routes/
│   └── schemas/
│
├── worker/
│   ├── tasks.py
│   └── ffmpeg_utils.py
│
├── storage/
│   └── videos/
│
├── docker/
│   ├── api.Dockerfile
│   ├── worker.Dockerfile
│
├── k8s/
│   ├── api-deployment.yaml
│   ├── worker-deployment.yaml
│   ├── redis.yaml
│
├── docker-compose.yml
└── README.md

🚀 Getting Started
Prerequisites

Docker

Docker Compose

Python 3.10+

FFmpeg installed locally (for dev mode)

Run Locally (Docker Compose)
docker-compose up --build


Services started:

FastAPI server

Redis

Worker containers

☸️ Kubernetes Deployment (Optional Advanced)
kubectl apply -f k8s/


Supports:

Horizontal pod scaling

Service discovery

Stateless deployments

🧪 Sample API Endpoints
Method	Endpoint	Description
POST	/upload	Upload a video
GET	/videos/{id}	Fetch metadata
GET	/stream/{id}/{resolution}	Stream video
🎯 Learning Outcomes

This project demonstrates:

Real-world backend architecture

Distributed task execution

Containerized microservices

Kubernetes fundamentals

Media processing pipelines

Production-grade system thinking
