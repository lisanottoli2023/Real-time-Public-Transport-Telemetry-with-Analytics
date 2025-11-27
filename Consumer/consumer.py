import os
import json
import time
import random
from datetime import datetime, timezone
from confluent_kafka import Consumer, KafkaError
import psycopg2

config = {
    "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"),
    "group.id": "bus-telemetry-consumer",
    "auto.offset.reset": "earliest"
}
consumer = Consumer(config)
consumer.subscribe(["bus.telemetry"])

DATABASE_URL = os.getenv("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS bus_telemetry (
    id SERIAL PRIMARY KEY,
    bus_id TEXT,
    timestamp TIMESTAMP,
    latitude FLOAT,
    longitude FLOAT,
    speed INT,
    passengers INT
);
""")
conn.commit()


def process_event(event: dict):
    cursor.execute("""
    INSERT INTO bus_telemetry (bus_id, timestamp, latitude, longitude, speed, passengers)
    VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        event["bus_id"],
        event["timestamp"],
        event["latitude"],
        event["longitude"],
        event["speed"],
        event["passengers"]
    ))
    conn.commit()
    print(f"Processed event: {event}")


print("Starting consumer...")
try:
    while True:
        try:
            msg = consumer.poll(timeout=1.0)
            
            if msg is None:
                continue
                
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:

                    print(f"Reached end of partition {msg.partition()}")
                else:
                    print(f"Consumer error: {msg.error()}")
                continue
            
            try:
                event_data = json.loads(msg.value().decode('utf-8'))
                process_event(event_data)
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON message: {e}")
            except KeyError as e:
                print(f"Missing required field in message: {e}")
            except Exception as e:
                print(f"Error processing message: {e}")
                
        except KeyboardInterrupt:
            print("Consumer interrupted by user")
            break
        except Exception as e:
            print(f"Unexpected error in consumer loop: {e}")
            time.sleep(1)  
            
finally:
    consumer.close()
    cursor.close()
    conn.close()
    print("Consumer stopped and resources cleaned up")