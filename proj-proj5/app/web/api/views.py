from django.shortcuts import render, redirect
from django.core import serializers
from .forms import CreateAccountForm, CreateListingForm, LoginForm, SearchForm
from django.http import JsonResponse, HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages 
import urllib
import urllib.request
import urllib.parse
import json

def home(request):
    req = urllib.request.Request('http://exp-api:8000/home/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)  
    context = {'meals': resp[0],'allcomments': resp[1]}
    return render(request, 'api/index.html', context)

def meal(request, cafe_id):
		req1 = urllib.request.Request('http://exp-api:8000/meal/'+ cafe_id)
		resp_json1 = urllib.request.urlopen(req1).read().decode('utf-8')
		resp = json.loads(resp_json1)
		context = {'resp': resp}
		return render(request, 'api/meal.html', context)

def comment(request, comment_id):
		req1 = urllib.request.Request('http://exp-api:8000/comment/'+ comment_id)
		resp_json1 = urllib.request.urlopen(req1).read().decode('utf-8')
		resp1 = json.loads(resp_json1)
		context1 = {'resp': resp1}
		return render(request, 'api/comment.html', context1)

def login(request):
	n = request.GET.get('next') or reverse('home')
	msg = False
	if request.method == 'GET':
		form = LoginForm()
		return render(request, 'api/login.html', {'form': form, 'next': n})
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if not form.is_valid():
			msg = "Missing input"
			return render(request, 'api/login.html', {'form': form, 'msg': msg})
		post = urllib.parse.urlencode(form.cleaned_data).encode('utf-8')
		req = urllib.request.Request('http://exp-api:8000/login', post)
		resp_json = urllib.request.urlopen(req).read().decode('utf-8')
		resp = json.loads(resp_json)
		if resp == "User Does Not Exist" or resp == "Incorrect password":
			msg = "Incorrect username/password"
			return render(request, 'api/login.html', {'form': form, 'msg': msg})
		req2 = urllib.request.Request('http://exp-api:8000/auth/check',post)
		resp2 = json.loads(urllib.request.urlopen(req2).read().decode('utf-8'))
		if resp2 == "Authenticator does not exist.":
			req3 = urllib.request.Request('http://exp-api:8000/auth/create',post)
			resp3 = json.loads(urllib.request.urlopen(req3).read().decode('utf-8'))
			authenticator = resp3['authenticator']
		else:
			authenticator = resp['authenticator']
		response = HttpResponseRedirect(n)
		response.set_cookie("authenticator", authenticator)
		return response

def logout(request):
    auth = request.COOKIES.get('authenticator')
    req = urllib.request.Request('http://exp-api:8000/logout/'+str(auth))
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    response = HttpResponseRedirect(reverse('login'))
    response.delete_cookie("authenticator")
    return response		

def create_listing(request):
	auth = request.COOKIES.get('authenticator')			

	if not auth:
		return HttpResponseRedirect(reverse("login") + "?next=" + reverse('create_listing'))
	if request.method == 'POST':
		form = CreateListingForm(request.POST)
		if form.is_valid():
			data = request.POST.dict()
			data['authenticator'] = auth
			post = urllib.parse.urlencode(data).encode('utf-8')
			try:
				req = urllib.request.Request('http://exp-api:8000/listing/create', data=post, method='POST')
			except ObjectDoesNotExist:
				return JsonResponse("Fail to create a new listing", safe=False)
			resp_json = urllib.request.urlopen(req).read().decode('utf-8')
			resp = json.loads(resp_json)
			return HttpResponseRedirect(reverse('home'))
		else:
			msg="Invalid input"
			return render(request, 'api/create_listing.html', {'form': form,'msg':msg})
	else:
		form = CreateListingForm()
	return render(request, 'api/create_listing.html', {'form': form})



def create_account(request):
	msg = False
	if request.method == 'GET':
		form = CreateAccountForm()
		return render(request, 'api/create_account.html', {'form': form})
	form = CreateAccountForm(request.POST)
	if not form.is_valid():
		msg = "Invalid input"
		return render(request, 'api/create_account.html', {'form': form, 'msg': msg})
	username = form.cleaned_data['username']
	email = form.cleaned_data['email']
	password = form.cleaned_data['password']
	post_data = {'username': username,
				 'email': email,
				 'password': password,}
	post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
	req = urllib.request.Request('http://exp-api:8000/create_account', data=post_encoded)
	resp = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
	if resp == "Duplicate username" or resp == "Duplicate email":
		msg = resp
		return render(request, 'api/create_account.html', {'form': form, 'msg': msg})
	else:
		msg = "Successfully created an account"
		return render(request, 'api/create_account.html', {'form': form, 'msg': msg})


def search_listing(request):
	search_res = None
	if request.method=='GET':
		form = SearchForm()
		return render(request, 'api/search_listing.html', {'search_form': form, 'res': search_res, 'firstvisit': True})
	form = SearchForm(request.POST)
	if not form.is_valid():
		return render(request, 'api/form_not_valid.html', {'search_form': form, 'res': search_res, 'firstvisit': False})
	post_data = {
		'query': form.cleaned_data['query']
	}
	post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
	req = urllib.request.Request('http://exp-api:8000/search/', data=post_encoded, method='POST')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	if resp['ok']:
		search_res = resp['result']
	return render(request, 'api/search_listing.html', {'search_form': form, 'res': search_res, 'firstvisit': False})













	