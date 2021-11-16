import sys
import os

from utils import PikaConnectorContextManager


def main():
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    with PikaConnectorContextManager("localhost") as cn:
        channel = cn.connection.channel()
        channel.queue_declare(queue="hello")
        # poniższe może się wysypąć jeśli nie ma kolejki == należy zabezpieczyć
        channel.basic_consume(queue="hello", auto_ack=True, on_message_callback=callback)
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
