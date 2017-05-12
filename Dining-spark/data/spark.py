from pyspark import SparkContext
import time
import MySQLdb

def split(pair):
	user_id = pair[0]
	items = pair[1]
	result = []
	for i in range(len(items)):
		for j in range(i+1, len(items)):
			result.append( (user_id, (items[i], items[j])) )
	return result

def update(a,b):
	cursor.execute("""SELECT item_id, recommended_items FROM api_recommendation WHERE item_id = %s""", (a))
	data = cursor.fetchone()
	string = str(b)
	if data == None:
		item = string + ","
		cursor.execute("""INSERT INTO api_recommendation (item_id, recommended_items) VALUES (%s, %s)""",(a, item))
	else:
		cursor.execute("""DELETE FROM api_recommendation WHERE item_id = %s""", (a))
		data2 = filter(None, data[1].split(","))
		if string not in list(data2):
			data2.append(string)
		item = ",".join(data2) + ","
		cursor.execute("""INSERT INTO api_recommendation (item_id, recommended_items) VALUES (%s, %s)""", (a, item))
	db.commit()

		
# Setup context
sc = SparkContext("spark://spark-master:7077", "PopularItems")


data = sc.textFile("/tmp/data/access.txt", 2)

#Read data in as pairs of (user_id, item_id clicked on by the user)
pairs = data.map(lambda line: tuple(line.split(",")))

#Group data into (user_id, list of item ids they clicked on)
distinctPairs = pairs.distinct().groupByKey()

#Sort values(user_id, (item_id1, item_id2 ...)) 
sortedPairs = distinctPairs.map(lambda pair: (pair[0], sorted(list(pair[1]))))

#Transform into (user_id, (item1, item2) where item1 and item2 are pairs of items the user clicked on
splittedPairs = sortedPairs.flatMap(lambda pair: split(pair))

# Transform into ((item1, item2), list of user1, user2 etc) where users are all the ones who co-clicked (item1, item2)
coclickedPairs = splittedPairs.map(lambda pair: (pair[1], 1))

# Transform into ((item1, item2), count of distinct users who co-clicked (item1, item2)
distinctCoclickedPairs = coclickedPairs.reduceByKey(lambda x, y: x + y)

#Filter out any results where less than 3 users co-clicked the same pair of items
massPairs = distinctCoclickedPairs.filter(lambda pair: pair[1] >= 3)

output = massPairs.collect()                          # bring the data back to the master node so we can print it out
for coview, count in sorted(output):
    print ("coviews: " + str(coview) + "\tcount: " + str(count))
print ("Popular items done")

db = MySQLdb.connect(host="db", user="www", passwd="$3cureUS", db="cs4501")
cursor = db.cursor()
cursor.execute("""TRUNCATE TABLE api_recommendation""")
for coviews, count in output:
	update(coviews[0],coviews[1])
	update(coviews[1],coviews[0])
print("Finished updating database")

cursor.close()
db.commit()
db.close()

sc.stop()