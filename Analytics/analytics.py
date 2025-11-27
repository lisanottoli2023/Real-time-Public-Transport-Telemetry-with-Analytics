import psycopg2
import os 
import time
from datetime import datetime, timezone


DATABASE_URL = os.getenv("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()



cursor.execute("""
CREATE TABLE IF NOT EXISTS bus_telemetry_metrics(
              id SERIAL PRIMARY KEY,
                bus_id TEXT,
                average_speed FLOAT,
                max_speed INT,
                total_passengers INT,
                event_per_minute INT,
                timestamp TIMESTAMP
);
""")
conn.commit()

def calculate_metrics():
    
    
    query = """
    SELECT bus_id,
           AVG(speed) AS average_speed,
           MAX(speed) AS max_speed,
           SUM(passengers) AS total_passengers,
           COUNT(*) AS event_count
    FROM bus_telemetry
    WHERE timestamp >= NOW() - INTERVAL '1 minute'
    GROUP BY bus_id;
    """
    
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        
        metrics_list = []
        current_time = datetime.now(timezone.utc)
        
        for row in results:
            metrics = {
                "bus_id": row[0],
                "average_speed": float(row[1]) if row[1] else 0.0,
                "max_speed": int(row[2]) if row[2] else 0,
                "total_passengers": int(row[3]) if row[3] else 0,
                "event_per_minute": int(row[4]) if row[4] else 0,
                "timestamp": current_time
            }
            metrics_list.append(metrics)
        
        return metrics_list
        
    except Exception as e:
        print(f"Error calculating metrics: {e}")
        return []


def store_metrics(metrics: dict):
    try:
        cursor.execute("""
        INSERT INTO bus_telemetry_metrics (bus_id, average_speed, max_speed, total_passengers, event_per_minute, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            metrics["bus_id"],
            metrics["average_speed"],
            metrics["max_speed"],
            metrics["total_passengers"],
            metrics["event_per_minute"],
            metrics["timestamp"]
        ))
        conn.commit()
        print(f"Stored metrics: {metrics}")
    except Exception as e:
        print(f"Error storing metrics: {e}")

def run_analytics():
    print("Starting analytics service...")
    
    while True:
        try:
            metrics_list = calculate_metrics()
            
            if metrics_list:
                print(f"Calculated metrics for {len(metrics_list)} buses")
                
                for metrics in metrics_list:
                    store_metrics(metrics)
            else:
                print("No data found for metrics calculation")
            
            print("Sleeping for 60 seconds...")
            time.sleep(60)
            
        except KeyboardInterrupt:
            print("Analytics service stopped by user")
            break
        except Exception as e:
            print(f"Error in analytics loop: {e}")
            time.sleep(60)



if __name__ == "__main__":
    run_analytics()


