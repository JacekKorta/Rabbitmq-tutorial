import sys

from utils import PikaConnectorContextManager

for _ in range(10):
    with PikaConnectorContextManager("localhost") as cn:
        channel = cn.connection.channel()
        channel.exchange_declare(exchange="logs", exchange_type="fanout")

        message = " ".join(sys.argv[1:]) or "info: Hello World!"
        channel.basic_publish(exchange="logs", routing_key="", body=message)
        print(" [x] Sent %r" % message)
