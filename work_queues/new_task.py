import pika

from utils import PikaConnectorContextManager

for i in range(20):
    with PikaConnectorContextManager("localhost") as cn:
        channel = cn.connection.channel()
        channel.queue_declare(queue="hello_tasks_durable", durable=True)
        # message = ' '.join(sys.argv[1:]) or "Hello World!"
        message = f"Task_D2 nr {i}{'...' * i}"
        channel.basic_publish(
            exchange="",
            routing_key="hello_tasks_durable",
            body=message,
            properties=pika.BasicProperties(delivery_mode=2),
        )
        print(" [x] Sent %r" % message)
