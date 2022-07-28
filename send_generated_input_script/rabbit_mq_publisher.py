import json
from config import rabbit_mq_config
import pika
from generators.model_generator import ModelGenerator


class RabbitMqPublisher:
    def __init__(self):
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_mq_config.HOST))
        self.channel = self._connection.channel()
        self.channel.queue_declare(queue=rabbit_mq_config.QUEUE)

    def publish(self, payload):
        self.channel.basic_publish(
            exchange=rabbit_mq_config.EXCHANGE,
            routing_key=rabbit_mq_config.ROUTING_KEY,
            body=str(payload)
        )

        print("Published Message:\n {}".format(payload))


if __name__ == "__main__":
    rabbitmq = RabbitMqPublisher()

    for i in range(20):
        input_student = f"""{json.dumps(ModelGenerator.generate_input_model().__dict__)}"""
        rabbitmq.publish(input_student)


