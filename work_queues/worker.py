import os
import sys
import time

from utils import PikaConnectorContextManager


def main():
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        time.sleep(body.count(b"."))
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    with PikaConnectorContextManager("localhost") as cn:
        channel = cn.connection.channel()
        channel.queue_declare(queue="hello_tasks_durable", durable=True)

        # bellow -> tylko jedno zadanie na raz
        channel.basic_qos(prefetch_count=1)
        # poniższe może się wysypąć jeśli nie ma kolejki == należy zabezpieczyć
        channel.basic_consume(queue="hello_tasks_durable", on_message_callback=callback)
        print(" [*] Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
