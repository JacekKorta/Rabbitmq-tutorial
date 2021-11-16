import random

from utils import PikaConnectorContextManager, color_list, severity_list


for _ in range(10):
    color = random.choice(color_list)
    severity = random.choice(severity_list)
    with PikaConnectorContextManager("localhost") as cn:
        channel = cn.connection.channel()
        channel.exchange_declare(exchange="topics_logs", exchange_type="topic")

        key = ".".join([severity, color])
        message = f"color: {color} and severity: {severity}| key={key}"
        channel.basic_publish(exchange="topics_logs", routing_key=key, body=message)
        print(" [x] Sent %r" % message)
