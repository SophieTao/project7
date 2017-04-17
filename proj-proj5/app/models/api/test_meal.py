from django.test import TestCase, Client    
from django.core.urlresolvers import reverse
from api import models
from .models import Cafe, Comment, Profile
import json

class CafeTestCase(TestCase):
        #setUp method is called before each test in this class
        def setUp(self):
           self.test_cafe = Cafe.objects.create(
                name = 'test',
                location='Runk',
                date="2017-02-14 21:19:07.831174",
                description='test',
                Calories = 300,
            )
        def test_invalid_url(self):
            response = self.client.get('/cafe/')
            self.assertEquals(response.status_code, 404)

        def test_valid_meal_list(self):
            response = self.client.get(reverse('cafe_list'))
            self.assertEqual(response.status_code, 200)

        def test_valid_meal_detail(self):
            url = reverse('retrieve_update_cafes', args=[self.test_cafe.id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            resp_json = json.loads((response.content).decode("utf-8"))
            self.assertEquals(resp_json["name"] , "test")
            self.assertEquals(resp_json["location"] , "Runk")
            self.assertEquals(resp_json["date"] , "2017-02-14T21:19:07.831Z")
            self.assertEquals(resp_json["description"] , "test")
            self.assertTrue(str(resp_json["Calories"]) == "300")
            
        def test_invalid_meal_detail(self):
            response = self.client.get(reverse('retrieve_update_cafes', args=[10000]))
            resp_json = (response.content).decode("utf-8")
            self.assertEqual(resp_json, '"Cafe does not exist."')
        
        def test_valid_create_meal(self):
            data = {"name": "test_create_meal","location":"l","date":"2017-02-14 21:19:07.831174","description":"test","Calories":3000}
            response = self.client.post(reverse("cafe-add"), data)
            resp_json = json.loads((response.content).decode("utf-8"))
            self.assertEquals(resp_json["name"] , "test_create_meal")
            self.assertEquals(resp_json["location"] , "l")
            self.assertEquals(resp_json["date"] , "2017-02-14 21:19:07.831174")
            self.assertEquals(resp_json["description"] , "test")
            self.assertTrue(str(resp_json["Calories"]) == "3000")
            #self.assertIn("test_create_meal",resp_json)
            
        def test_invalid_create_meal1(self):
            wrongdata = {"location":"l","date":"2017-02-14 21:19:07.831174","description":"test","Calories":3000}
            response = self.client.post(reverse('cafe-add'), wrongdata)
            resp_json = (response.content).decode("utf-8")
            self.assertEquals(resp_json, '"Input did not contain all the required fields."')
        
        def test_invalid_create_meal2(self):
            wrongdata = {"name": "test_create_meal","date":"2017-02-14 21:19:07.831174","description":"test","Calories":3000}
            response = self.client.post(reverse('cafe-add'), wrongdata)
            resp_json = (response.content).decode("utf-8")
            self.assertEquals(resp_json, '"Input did not contain all the required fields."')

        def test_invalid_create_meal3(self):
            wrongdata = {"name": "test_create_meal","location":"l","description":"test","Calories":3000}
            response = self.client.post(reverse('cafe-add'), wrongdata)
            resp_json = (response.content).decode("utf-8")
            self.assertEquals(resp_json, '"Input did not contain all the required fields."')

        def test_invalid_create_meal4(self):
            wrongdata = {"name": "test_create_meal","location":"l", "date":"2017-02-14 21:19:07.831174","Calories":3000}
            response = self.client.post(reverse('cafe-add'), wrongdata)
            resp_json = (response.content).decode("utf-8")
            self.assertEquals(resp_json, '"Input did not contain all the required fields."')

        def test_invalid_create_meal4(self):
            wrongdata = {"name": "test_create_meal","location":"l", "date":"2017-02-14 21:19:07.831174","description":"test"}
            response = self.client.post(reverse('cafe-add'), wrongdata)
            resp_json = (response.content).decode("utf-8")
            self.assertEquals(resp_json, '"Input did not contain all the required fields."')

        def test_valid_edit_meal(self):
            response = self.client.post(reverse('retrieve_update_cafes', args=[self.test_cafe.id]), {'name': "test_update_meal","location": "edited", "date":"2017-02-14 21:19:07.831174","description":"test","Calories":3000})
            resp_json = json.loads((response.content).decode("utf-8"))
            self.assertEquals(resp_json["name"] , "test_update_meal")
            self.assertEquals(resp_json["location"] , "edited")
            self.assertEquals(resp_json["date"] , "2017-02-14 21:19:07.831174")
            self.assertEquals(resp_json["description"] , "test")
            self.assertTrue(str(resp_json["Calories"]) == "3000")
            #self.assertEquals(resp_json, "Updated task")

        def test_invalid_edit_meal(self):
            wrongdata = {"name": "test_create_meal","location": "hello","date":"2017-02-14","description":"test","Calories":"300"}
            response = self.client.post(reverse('retrieve_update_cafes', args=[10000]), wrongdata)
            resp_json = (response.content).decode("utf-8")
            self.assertEquals(resp_json, '"Cafe does not exist."')

        def test_valid_delete_meal(self):
            deleteresponse = self.client.post(reverse('cafe-delete', args=[self.test_cafe.id]))
            resp_json = (deleteresponse.content).decode("utf-8")
            self.assertEquals(resp_json, '"Deleted meal"')
            #duplicate deletes
            deleteresponse2 = self.client.post(reverse('cafe-delete', args=[self.test_cafe.id]))
            resp2_json = (deleteresponse2.content).decode("utf-8")
            self.assertEquals(resp2_json, '"This meal does not exist."')

        def test_invalid_delete_meal(self):
            response = self.client.post(reverse('cafe-delete', args=[10000]))
            resp_json = (response.content).decode("utf-8")
            self.assertEquals(resp_json, '"This meal does not exist."')

        def tearDown(self):
            pass #nothing to tear down


        

