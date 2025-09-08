import pika
import json
import os
from dotenv import load_dotenv

load_dotenv()


class RabbitMQClient:
    def __init__(self, host='localhost'):
        self.host = host
        self.user = os.getenv('RABBITMQ_USER', 'user')
        self.password = os.getenv('RABBITMQ_PASSWORD', 'password')
        self.port = int(os.getenv('RABBITMQ_PORT', 5672))
        credentials = pika.PlainCredentials(self.user, self.password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port, credentials=credentials))
        self.channel = self.connection.channel()
        # Declare a topic exchange
        self.channel.exchange_declare(exchange='alerts_exchange', exchange_type='topic')

    def publish_alert(self, source, alert_data):
        routing_key = f'alerts.{source}'
        message = json.dumps(alert_data)
        self.channel.basic_publish(
            exchange='alerts_exchange',
            routing_key=routing_key,
            body=message
        )
        print(f" [x] Sent '{message}' with routing key '{routing_key}'")

    def __del__(self):
        self.connection.close()