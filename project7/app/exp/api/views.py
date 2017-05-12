from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core import serializers
from django.utils import timezone,dateparse
import datetime
from datetime import timedelta
import urllib.request
import urllib.parse
import json
from kafka import KafkaProducer
from elasticsearch import Elasticsearch
from django.core.exceptions import ObjectDoesNotExist


def home(request):
	#req = urllib.request.Request('http://models-api:8000/api/v1/meals/2')
	req = urllib.request.Request('http://models-api:8000/api/v1/allcomments')	
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)

	req1 = urllib.request.Request('http://models-api:8000/api/v1/recentmeals')
	resp_json1 = urllib.request.urlopen(req1).read().decode('utf-8')
	resp1 = json.loads(resp_json1)

	req2 = urllib.request.Request('http://models-api:8000/api/v1/allmeals')
	resp_json2 = urllib.request.urlopen(req2).read().decode('utf-8')
	resp2 = json.loads(resp_json2)
	

	if len(resp1) < 3:
		return JsonResponse([resp2, resp],safe=False)
	else:
		return JsonResponse([resp1, resp],safe=False)

def meal(request, cafe_id):
	req = urllib.request.Request('http://models-api:8000/api/v1/meals/' + cafe_id)
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	recommendations = urllib.request.Request('http://models-api:8000/api/v1/recommendations/retrieve/'+cafe_id)
	resp_json1 = urllib.request.urlopen(recommendations).read().decode('utf-8')
	resp1 = json.loads(resp_json1)
	if resp1 == "recommended items do not exist.":
		resp['recommended_items'] = ""
		return JsonResponse(resp, safe=False)
	resp['recommended_items'] = resp1['recommended_items']
	recs = []
	for i in list(filter(None,resp['recommended_items'].split(","))):
		req2 = urllib.request.Request('http://models-api:8000/api/v1/meals/' + i)
		resp_json2 = urllib.request.urlopen(req2).read().decode('utf-8')
		resp2 = json.loads(resp_json2)
		recs.append(resp2['name'])
	resp['rec'] = recs
	# message = json.dumps([{'user': str(resp), 'cafe': str(cafe_id)}, 'coview']).encode('utf-8')
	# kafka_producer = KafkaProducer(bootstrap_servers='kafka_container:9092')
	# kafka_producer.send("cafe_topic", message)
	return JsonResponse(resp, safe=False)


def comment(request, comment_id):
	req = urllib.request.Request('http://models-api:8000/api/v1/comments/' + comment_id)
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	return JsonResponse(resp, safe=False)
	
# def profile(request, profile_id):
# 	req = urllib.request.Request('http://models-api:8000/api/v1/profiles/' + profile_id)
# 	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
# 	resp = json.loads(resp_json)
# 	return JsonResponse([resp], safe=False)

############## user management (login, logout, create account) ###############
def login(request):
	if request.method == "POST":	
		post = request.POST.dict()
		data = urllib.parse.urlencode(post).encode('utf-8')
		req = urllib.request.Request('http://models-api:8000/api/v1/auth/create', data)
		# except ObjectDoesNotExist:
		# 	return JsonResponse("Fail to login", safe=False)	
		resp_json = urllib.request.urlopen(req).read().decode('utf-8')
		resp = json.loads(resp_json)
		return JsonResponse(resp, safe=False)

	

def logout(request,authenticator):
	# if request.method == "POST":
	# 	post = request.POST.dict()
	# 	post_encoded = urllib.parse.urlencode(post).encode('utf-8')
	try:
		req = urllib.request.Request('http://models-api:8000/api/v1/auth/delete/' + str(authenticator))

	except ObjectDoesNotExist:
		return JsonResponse("User not found", safe=False)	
	resp_json = urllib.request.urlopen(req).read().decode('utf-8') 
	resp = json.loads(resp_json)
	return JsonResponse(resp,safe=False)
	# for i in resp:
	# 		try:
	# 			r = urllib.request.Request('http://models-api:8000/api/v1/auth/delete/' + str(i["authenticator"]))
	# 		except ObjectDoesNotExist:
	# 			return JsonResponse("Cannot delete authenticator", safe=False)	
	# 		resp_json2 = urllib.request.urlopen(r).read().decode('utf-8')
	# 	return JsonResponse("Successfully logout", safe=False)
	# # else:
	# 	return JsonResponse("Must Post", safe=False)

def create_account(request):
	if request.method == "POST":
		post = request.POST.dict()
		data = urllib.parse.urlencode(post).encode('utf-8')
		req0 = urllib.request.Request('http://models-api:8000/api/v1/profiles/check', data=data)
		resp_json0 = urllib.request.urlopen(req0).read().decode('utf-8')
		resp0 = json.loads(resp_json0)
		if resp0 == "Duplicate username" or resp0 == "Duplicate email":
			return JsonResponse(resp0,safe=False)
		req = urllib.request.Request('http://models-api:8000/api/v1/profiles/create', data)
		resp_json = urllib.request.urlopen(req).read().decode('utf-8')
		resp = json.loads(resp_json)
		if resp == "Input did not contain all the required fields." or resp == "unique":
			return JsonResponse(resp, safe=False)
		else:
			auth = urllib.parse.urlencode(post).encode('utf-8')
			req = urllib.request.Request('http://models-api:8000/api/v1/auth/create', auth)
		try:
			resp2 = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
		except ObjectDoesNotExist:
			return JsonResponse("Cannot create authenticator", safe=False)
		return JsonResponse(resp2, safe=False)


def delete_expired_auth(request):
    # post = request.POST.dict()
    # data = urllib.parse.urlencode(post).encode('utf-8')
    req = urllib.request.Request('http://models-api:8000/api/v1/auths')    				
    try:
    	resp = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))		
    except ObjectDoesNotExist:
    	return JsonResponse("Invalid authenticator.", safe=False)
    # return JsonResponse(resp,safe=False)
    for auth in resp:
    	a = auth["authenticator"]
    	if auth['date_created'] <= (timezone.now() - datetime.timedelta(seconds=10)).isoformat():
    		# return JsonResponse("expired",safe=False)
    		# r = urllib.request.Request('http://models-api:8000/api/v1/auth/delete/' + str(a))
    		r1 = urllib.request.Request('http://models-api:8000/api/v1/auth/delete/' + str(a))
    		# req = urllib.request.Request('http://models-api:8000/api/v1/auth/check',auth)    	
    		resp2 = json.loads(urllib.request.urlopen(r1).read().decode('utf-8'))		
    		# return JsonResponse(resp2,safe=False)
    req2 = urllib.request.Request('http://models-api:8000/api/v1/auths')     
    resp2 = json.loads(urllib.request.urlopen(req2).read().decode('utf-8'))		
    return JsonResponse(resp2, safe=False)

    	# return JsonResponse("expired",safe=False)
    # 	resp = json.loads(resp_json)
    # 	for i in resp:
    # 		try:
    # 		except ObjectDoesNotExist:
    # 			return JsonResponse("Cannot delete expired authenticator", safe=False)	
    # 		return JsonResponse("Expired authenticator.", safe=False)
    # else:
    	# return JsonResponse("Valid authenticator.", safe=False)

    # 	def getAuthUser(request):
    # post = request.POST.dict()
    # data = urllib.parse.urlencode(post).encode('utf-8')
    # req = urllib.request.Request('http://models-api:8000/api/v1/auth/check',data)    				
    # try:
    # 	resp = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))		
    # except ObjectDoesNotExist:
    # 	return JsonResponse("Invalid authenticator.", safe=False)
    # if resp['date_created'] <= (timezone.now() - datetime.timedelta(minutes=1)).isoformat():
    # 	return JsonResponse("expired",safe=False)
    # 	resp = json.loads(resp_json)
    # 	for i in resp:
    # 		try:
    # 			r = urllib.request.Request('http://models-api:8000/api/v1/auth/delete/' + str(i["authenticator"]))
    # 		except ObjectDoesNotExist:
    # 			return JsonResponse("Cannot delete expired authenticator", safe=False)	
    # 		return JsonResponse("Expired authenticator.", safe=False)
    # else:
    # 	return JsonResponse("Valid authenticator.", safe=False)

    
def check_auth(request):
	post = request.POST.dict()
	data = urllib.parse.urlencode(post).encode('utf-8')
	req = urllib.request.Request('http://models-api:8000/api/v1/auth/check',data)
	resp = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
	if resp == "Authenticator does not exist.":
		return JsonResponse("Authenticator does not exist.", safe=False)	
		#return JsonResponse("Authenticate failed.", safe=False)
	return JsonResponse(resp)	

def get_auth(request):
	post = request.POST.dict()
	data = urllib.parse.urlencode(post).encode('utf-8')	
	req = urllib.request.Request('http://models-api:8000/api/v1/auth/get',data)
	resp = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
	if resp == "Authenticator does not exist.":
		return JsonResponse("Authenticator does not exist.", safe=False)	
		#return JsonResponse("Authenticate failed.", safe=False)
	return JsonResponse(resp)	

def create_auth(request):
	post = request.POST.dict()
	data = urllib.parse.urlencode(post).encode('utf-8')
	req = urllib.request.Request('http://models-api:8000/api/v1/auth/create',data)
	try:
		resp2 = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
	except ObjectDoesNotExist:
		return JsonResponse("Cannot create authenticator", safe=False)
	return JsonResponse(resp2, safe=False)

def check_dup(request):
	post = request.POST.dict()
	data = urllib.parse.urlencode(post).encode('utf-8')
	req = urllib.request.Request('http://models-api:8000/api/v1/profiles/check',data)
	resp = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
	return JsonResponse(resp,safe=False)	

########################################

def create_listing(request):
	if request.method == "POST":
		post = request.POST.dict()
		data = urllib.parse.urlencode(post).encode('utf-8')
		req = urllib.request.Request('http://models-api:8000/api/v1/auth/check',data)
		resp = urllib.request.urlopen(req).read().decode('utf-8')
		if resp == "Authenticator does not exist.":
			return JsonResponse("Only authenticated users can create new listings.", safe=False)
		
		data = urllib.parse.urlencode(post).encode('utf-8')
		req2 = urllib.request.Request('http://models-api:8000/api/v1/meals/create', data)
		try:
			resp2 = json.loads(urllib.request.urlopen(req2).read().decode('utf-8'))
			listing_info = resp2['result']
			listing_info['id'] = resp2['id']
			producer = KafkaProducer(bootstrap_servers='kafka:9092')
			producer.send('new-listings-topic', json.dumps(listing_info).encode('utf-8'))
			print(listing_info)
		except KeyError:
			return JsonResponse("Cannot create new listing", safe=False)
		return JsonResponse(listing_info, safe=False)
	else:
		return HttpResponse("Must Post")


def search_listing(request):
	response = {'ok': False, 'result': []}
	if request.method == 'GET':
	    response['ok'] = "Invalid. Expecting POST request."
	else:
		query = request.POST['query']
		es = Elasticsearch(['es'])
		search_response = es.search(index='listing_index', body={'query': {'query_string': {'query': query}}})
		response['ok'] = True
		for hit in search_response['hits']['hits']:		
			response['result'].append(hit['_source'])
	return JsonResponse(response)




