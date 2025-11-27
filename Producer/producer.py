import os
import json
import time
import random
from datetime import datetime, timezone
from confluent_kafka import Producer

config = {
    "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"),
    "client.id": "bus-telemetry-producer"
}

LAT_BASE = ("LAT_BASE", "52.5200")
LON_BASE = ("LON_BASE", "13.4050")

producer = Producer(config)

def send_event(event: dict):
    producer.produce(
        "bus.telemetry",
        json.dumps(event).encode("utf-8")
    )
    producer.poll(0)  
    print(f"Sent event: {event}")

count = 0
while True : 
    message = {
        "bus_id": "BUS-1",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "latitude": float(LAT_BASE[1]) + random.uniform(-0.01, 0.01),
        "longitude": float(LON_BASE[1]) + random.uniform(-0.01, 0.01),
        "speed": random.randint(0, 70),
        "passengers": random.randint(0, 80),
    }

    send_event(message)
    count += 1
    if count % 10 == 0: 
        print(f"Sent {count} telemetry events")
    time.sleep(1)