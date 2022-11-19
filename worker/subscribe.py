import logging
from concurrent import futures
import os
from google.cloud import pubsub_v1

logging.basicConfig(level=logging.INFO)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= 'pub-sub.json'
project_id = "cloud-convertion-tool"
subscription_id = "cloud-convertion-tool-sub"

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_id}`
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message):
    logging.info("Received %s", message)
    message.ack()

future = subscriber.subscribe(subscription_path, callback=callback)
with subscriber:
    try:
        future.result()
    except KeyboardInterrupt:
        future.cancel()  # Trigger the shutdown.
        future.result()  
