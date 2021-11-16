from utils import PikaConnectorContextManager, color_list


def callback(ch, method, properties, body):
    print(" [x] %r" % body)


with PikaConnectorContextManager("localhost") as cn:

    channel = cn.connection.channel()

    # exchange options are: : direct, topic, headers and fanout
    channel.exchange_declare(exchange="direct_logs", exchange_type="direct")
    # tworzy tymczasową kolejkę arg[0] - da losową nazwę, [arg[1] usunię nieuzywaną kolejke
    result = channel.queue_declare(queue="", exclusive=True)

    queue_name = result.method.queue

    for color in color_list:
        channel.queue_bind(exchange="direct_logs", queue=queue_name, routing_key=color)

    print(" [*] Waiting for logs. To exit press CTRL+C")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()
