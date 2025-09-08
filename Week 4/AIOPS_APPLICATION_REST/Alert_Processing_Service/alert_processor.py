import pika
import json
import sqlite3
import csv
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# --- CSV & DB Helpers ---
def load_csv_data(filepath):
    data = {}
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data[row['host']] = row
    return data

def is_in_maintenance(host, maintenance_data):
    if host in maintenance_data:
        # Assuming maintenance_data has 'start_time' and 'end_time' fields
        now = datetime.now()
        start = datetime.strptime(maintenance_data[host]['start_time'], "%Y-%m-%d %H:%M")
        end = datetime.strptime(maintenance_data[host]['end_time'], "%Y-%m-%d %H:%M")
        return start <= now <= end
    return False

def setup_db():
    conn = sqlite3.connect('alerts.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS processed_alerts (
            id INTEGER PRIMARY KEY,
            source TEXT,
            host TEXT,
            message TEXT,
            severity TEXT,
            team TEXT,
            owner TEXT,
            maintenance INTEGER,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_alert_to_db(alert):
    conn = sqlite3.connect('alerts.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO processed_alerts (source, host, message, severity, team, owner, maintenance, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        alert['source'],
        alert['host'],
        alert['message'],
        alert['severity'],
        alert['team'],
        alert['owner'],
        alert['maintenance'],
        alert['timestamp']
    ))
    conn.commit()
    conn.close()

# --- Main Consumer Logic ---
def callback(ch, method, properties, body):
    raw_alert = json.loads(body)
    
    # Normalization
    normalized_alert = {}
    if raw_alert.get('source') == 'rest':
        normalized_alert = {
            "source": "rest",
            "host": raw_alert.get('host'),
            "message": raw_alert.get('message'),
            "severity": raw_alert.get('severity')
        }
    elif raw_alert.get('source') == 'grafana':
        normalized_alert = {
            "source": "grafana",
            "host": raw_alert.get('host'),
            "message": raw_alert.get('description'), # Mapping Grafana's 'description' to 'message'
            "severity": raw_alert.get('level') # Mapping 'level' to 'severity'
        }
    elif raw_alert.get('source', 'grafanav2') == 'grafanav2':
        normalized_alert = raw_alert
        normalized_alert["source"] = "grafanav2"
        normalized_alert["host"] = raw_alert.get('commonLabels', {}).get('instance', 'host_not_found')
        normalized_alert["message"] = raw_alert.get('message', 'message_not_defined')
        normalized_alert["severity"] = raw_alert.get('status', 'status_not_defined')
    
    # Enrichment
    host = normalized_alert.get('host', 'host not found')
    enrichment_data = load_csv_data('enrichment_data.csv')
    maintenance_data = load_csv_data('maintenance_data.csv')
    
    if host in enrichment_data:
        normalized_alert['team'] = enrichment_data[host].get('team')
        normalized_alert['owner'] = enrichment_data[host].get('owner')
    else:
        normalized_alert['team'] = 'unknown'
        normalized_alert['owner'] = 'unknown'

    # Maintenance check
    normalized_alert['maintenance'] = is_in_maintenance(host, maintenance_data)
    
    # Add timestamp
    normalized_alert['timestamp'] = datetime.now().isoformat()
    
    print(" [x] Processed and stored alert:")
    print(normalized_alert)
    insert_alert_to_db(normalized_alert)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consuming():
    setup_db()
    user = os.getenv('RABBITMQ_USER', 'user')
    password = os.getenv('RABBITMQ_PASSWORD', 'password')
    port = int(os.getenv('RABBITMQ_PORT', 5672))
    credentials = pika.PlainCredentials(user, password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=port, credentials=credentials))
    channel = connection.channel()

    # Declare the same exchange as the producer
    channel.exchange_declare(exchange='alerts_exchange', exchange_type='topic')
    
    # Create a queue and bind it to consume all alerts
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='alerts_exchange', queue=queue_name, routing_key='alerts.#')

    print(' [*] Waiting for alerts. To exit press CTRL+C')
    
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback
    )
    
    channel.start_consuming()

if __name__ == '__main__':
    start_consuming()