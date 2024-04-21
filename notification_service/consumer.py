import pika
from firebase_config import config
import sys, os

# use fcm for notification service
# one end is connected to this service and another end to order service
def main():
    connectionParameter = pika.ConnectionParameters(host= os.getenv("RABBITMQ_HOST"))
    connection = pika.BlockingConnection(parameters= connectionParameter)
    channel = connection.channel()

    channel.queue_declare(queue= os.getenv("QUEUE_NAME"))
    def callback(ch, method, properties, body):
        print(body)
        admin = config.admin_init()

    channel.basic_consume(queue='', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


        