from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json
from time import sleep

print("test\ntest\ntest\ntest\ntest\ntest")
sleep(20)
print("haha")

# Pull messages from kafka
consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
es = Elasticsearch(['es'])

print("before for loop")
print(consumer)
for message in consumer:
    print("in for loop")
    new_listing = json.loads((message.value).decode('utf-8'))
    # Index the message in elastic search

    es.index(index='listing_index', doc_type='listing', id=new_listing['id'], body=new_listing)
    print(new_listing['name'])
    # Commit the changes to the index files
    es.indices.refresh(index="listing_index")
