import sys

from utils import PikaConnectorContextManager


def callback(ch, method, properties, body):
    print(" [x] %r" % body)


with PikaConnectorContextManager("localhost") as cn:

    channel = cn.connection.channel()

    # exchange options are: : direct, topic, headers and fanout
    channel.exchange_declare(exchange="topics_logs", exchange_type="topic")
    # tworzy tymczasową kolejkę arg[0] - da losową nazwę, [arg[1] usunię nieuzywaną kolejke
    result = channel.queue_declare(queue="", exclusive=True)

    queue_name = result.method.queue

    binding_key = sys.argv[1]
    if not binding_key:
        binding_key = "*.*"
    print(f"Usage: {binding_key} - binding key")

    channel.queue_bind(exchange="topics_logs", queue=queue_name, routing_key=binding_key)

    print(" [*] Waiting for logs. To exit press CTRL+C")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()
