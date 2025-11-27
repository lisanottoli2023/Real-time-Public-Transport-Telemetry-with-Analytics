# Real-time-Public-Transport-Telemetry-with-Analytics
Data engineering project with kafka

                 ┌────────────────────────┐
                 │     Data Generator     │
                 │ (Producer - Python)    │
                 │  Generates Bus Events  │
                 └─────────────┬──────────┘
                               │
                               ▼
                   ┌──────────────────────┐
                   │        Kafka         │
                   │   bus.telemetry      │
                   │  (Message Broker)    │
                   └─────────────┬────────┘
                               │
                               ▼
               ┌────────────────────────────┐
               │        Consumer            │
               │  Reads events from Kafka   │
               │ Inserts into PostgreSQL DB │
               └─────────────┬──────────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │       PostgreSQL        │
                  │  bus_telemetry table    │
                  │ Stores raw telemetry    │
                  └─────────────┬──────────┘
                               │
                               ▼
             ┌────────────────────────────────────┐
             │             Analytics               │
             │  - Reads DB every minute            │
             │  - Calculates averages, max speed   │
             │  - Inserts into metrics table       │
             │  - Exposes Prometheus metrics       │
             │        (/metrics)                   │
             └──────────────────┬──────────────────┘
                                │
                                ▼
                    ┌──────────────────────┐
                    │     Prometheus       │
                    │Scrapes analytics svc │
                    │  Collects metrics    │
                    └───────────┬──────────┘
                                │
                                ▼
                    ┌──────────────────────┐
                    │       Grafana        │
                    │  Dashboards (Speed,  │
                    │ Events, Passengers…) │
                    └──────────────────────┘

What i learned during this project : 

1. Data Engineering Fundamentals

Learned how event-driven architectures work.

Understood the concepts of producers, consumers, brokers, topics, partitions, and offsets.

Learned how data flows through a streaming pipeline instead of classic batch processing.


2. Kafka Messaging System

Learned how to:

Create Kafka producers and consumers.

Publish messages to topics.

Subscribe and consume messages correctly.


3. Microservices Architecture

Learned to structure a system into independent services:

Producer service

Consumer service

Analytics service

Understood how microservices communicate through a message broker.


4. Docker & Containerization

Containerize applications using Dockerfiles.

Build images for each microservice.

Push images to Docker Hub.

Integrate services into docker-compose

Use Docker networks so containers can talk to each other.

Understand Docker concepts: images, containers, layers, volumes, networks.


5. CI/CD Pipelines w/(GitHub Actions)

Built a full CI/CD Workflow:

Code checkout

Install Python with uv

Run tests with pytest

Build Docker images

Push to Docker Hub

Automatic Git version tagging


7. Analytics & Data Processing

Learned to process consumed Kafka messages for analytics.

Understood:

Stream processing basics

Basic transformations and aggregations

How analytics integrates into a real-time workflow


9. Architecture Thinking

Learned to design:

A streaming data pipeline

A multi-service architecture

A communication flow between services and Kafka

Became able to explain the system end-to-end with diagrams.

