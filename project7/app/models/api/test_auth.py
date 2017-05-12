from django.test import TestCase, Client    
from django.core.urlresolvers import reverse
from api import models
from .models import Cafe, Comment, Profile, Authenticator
import json

class AuthenticatorTestCase(TestCase):
        #setUp method is called before each test in this class
        def setUp(self):
           self.test_auth = Profile.objects.create(
                username = 'test',
                password='test',
                email="test@gmail.com",
            )
                      
        
        def test_invalid_url(self):
            response = self.client.get('/auth/')
            self.assertEquals(response.status_code, 404) 

        def test_valid_all_auth(self):
            response = self.client.get(reverse('get_all_auth'))
            self.assertEqual(response.status_code, 200)

        def test_valid_create_auth(self):
            data = {"username": "Dan", "password": "Dan", "email": "Dan@gmail.com"}
            response = self.client.post(reverse("create_auth"), data)            
            resp_json = (response.content).decode("utf-8")
            self.assertEquals(resp_json, '"User Does Not Exist"')    
            response = self.client.post(reverse("profile-add"), data)
            response2 = self.client.post(reverse("create_auth"), data)            
            resp_json2 = json.loads((response2.content).decode("utf-8"))
            self.assertTrue(resp_json2["authenticator"])
            self.assertTrue(resp_json2["date_created"])
            self.assertTrue(resp_json2["user_id"])

        def test_invalid_create_auth_pw(self):
            data = {"username": "Dan", "password": "Dan", "email": "Dan@gmail.com"}
            response = self.client.post(reverse("profile-add"), data)
            response2 = self.client.post(reverse("create_auth"), data) 
            wrongdata = {"username": "Dan", "password": "Dan1", "email": "Dan@gmail.com"}
            response = self.client.post(reverse('create_auth'), wrongdata)
            resp_json = (response.content).decode("utf-8")
            self.assertEquals(resp_json, '"Incorrect password"')

        def test_invalid_create_auth_name(self):
            data = {"username": "Dan", "password": "Dan", "email": "Dan@gmail.com"}
            response = self.client.post(reverse("profile-add"), data)
            response2 = self.client.post(reverse("create_auth"), data) 
            wrongdata = {"username": "Dan1", "password": "Dan", "email": "Dan@gmail.com"}
            response = self.client.post(reverse('create_auth'), wrongdata)
            resp_json = (response.content).decode("utf-8")
            self.assertEquals(resp_json, '"User Does Not Exist"')
        
        def test_invalid_check_auth(self):
            data = {"username": "Dan", "password": "Dan", "email": "Dan@gmail.com"}
            response = self.client.post(reverse("profile-add"), data)
            response2 = self.client.post(reverse("create_auth"), data)
            wrongdata = {"username": "Dan1", "password": "Dan", "email": "Dan@gmail.com"}
            response3 = self.client.post(reverse("check_auth"), wrongdata)
            resp_json = (response3.content).decode("utf-8")
            self.assertEquals(resp_json, '"Authenticator does not exist."')

        def test_valid_check_auth(self):
            data = {"username": "Dan", "password": "Dan", "email": "Dan@gmail.com"}
            response = self.client.post(reverse("profile-add"), data)
            response2 = self.client.post(reverse("create_auth"), data)
            response3 = self.client.post(reverse("check_auth"), data)
            resp_json = json.loads((response3.content).decode("utf-8"))
            self.assertTrue(resp_json["authenticator"])
            self.assertTrue(resp_json["date_created"])
            self.assertTrue(resp_json["user_id"])

        def test_delete_auth(self):
            data = {"username": "Dan", "password": "Dan", "email": "Dan@gmail.com"}
            response = self.client.post(reverse("profile-add"), data)
            response2 = self.client.post(reverse("create_auth"), data)
            resp_json2 = json.loads((response2.content).decode("utf-8"))
            response3 = self.client.post('/api/v1/auth/delete/' +str(resp_json2["authenticator"]))
            resp_json3 = (response3.content).decode("utf-8")
            self.assertEquals(resp_json3, '"Successfully deleted user authentication"')            
            response4 = self.client.post('/api/v1/auth/delete/' +str(resp_json2["authenticator"])) 
            resp_json4 = (response4.content).decode("utf-8")
            self.assertEquals(resp_json4, '"User has not  been authenticated yet."')

        def tearDown(self):
            pass #nothing to tear down


        

