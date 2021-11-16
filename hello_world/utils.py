import pika


class PikaConnectorContextManager:
    def __init__(self, hostname):
        self.hostname = hostname
        self.connection = None

    def __enter__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.hostname))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
