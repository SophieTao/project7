from kafka import KafkaConsumer
from kafka.common import NodeNotReadyError
import json
import sys
import time
from time import sleep

# print("test\ntest\ntest\ntest\ntest\ntest")
sleep(20)
# print("haha")

# Pull messages from kafka
consumer = None 
while not consumer:
	try:
		consumer = KafkaConsumer('recommendation-topic', group_id='recommendations-indexer', bootstrap_servers=['kafka:9092'])
	except NodeNotReadyError:
		time.sleep(100)

# print("before for loop")
# print(consumer)
while True: 
	# with open('data/access.txt', 'a') as file:
	#     	file.write("\n")
	for message in consumer:
	    print("in for loop")
	    new_listing = json.loads((message.value).decode('utf-8'))
	    data = str(new_listing['user_id']) + "," + str(new_listing['item_id'])+"\n"
	    with open('data/access.txt', 'a') as file:
	    	file.write(data)
	    # Commit the changes to the index files
