import pika
from read.reader import Reader
from config import rabbit_mq_config


class RabbitMqReader(Reader):
    def __init__(self):
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_mq_config.HOST))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=rabbit_mq_config.QUEUE)
        print("Server started...")
        print("[X] Waiting for data...")

    def listen(self, callback):
        self._channel.basic_consume(
            queue=rabbit_mq_config.QUEUE,
            on_message_callback=lambda ch, method, properties, body: callback(body),
            auto_ack=True
        )
        self._channel.start_consuming()
