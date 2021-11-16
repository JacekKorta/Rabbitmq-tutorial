import random
import sys

from utils import PikaConnectorContextManager, color_list


for _ in range(10):
    color = random.choice(color_list)
    with PikaConnectorContextManager("localhost") as cn:
        channel = cn.connection.channel()
        channel.exchange_declare(exchange="direct_logs", exchange_type="direct")

        message = " ".join(sys.argv[1:]) or f"info: {color}"
        channel.basic_publish(exchange="direct_logs", routing_key=color, body=message)
        print(" [x] Sent %r" % message)
