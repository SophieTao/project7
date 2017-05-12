from django.test import TestCase, Client    
from django.core.urlresolvers import reverse
from api import models
from .models import Cafe, Comment, Profile, Recommendation
import json

class RecommendationTestCase(TestCase):
        #setUp method is called before each test in this class
        def setUp(self):
            self.test_recommendation = Recommendation.objects.create(
            recommended_items = "8,6,7,9,",
            item_id= 4,
            )
        def test_retrieve_recommendations(self):
            response = self.client.get(reverse('retrieve_recommendations', args=[self.test_recommendation.item_id]))
            self.assertEqual(response.status_code, 200)
            resp_json = json.loads((response.content).decode("utf-8"))
            self.assertEquals(resp_json["recommended_items"] , "8,6,7,9,")
            self.assertTrue(str(resp_json["item_id"]) == "4")

        def test_invalid_create_recommendations(self):
            wrongdata = {"recommended_items":"1,2,3,"}
            response = self.client.post(reverse('create_recommendations'), wrongdata)
            self.assertEqual(response.status_code, 200)
            resp_json = (response.content).decode("utf-8")
            self.assertEquals(resp_json, '"Meal does not exist"')

        def test_valid_create_recommendations(self):
            data = {"recommended_items":"8,6,7,9,","item_id":4}
            response = self.client.post(reverse('create_recommendations'), data)
            self.assertEqual(response.status_code, 200)
            resp_json = (response.content).decode("utf-8")
            self.assertEquals(resp_json, '"Successfully created the recommended item"')

        def test_invalid_delete_recommendations(self):
              data = {"item_id":10000}
              response = self.client.post(reverse('delete_recommendations'), data)
              resp_json = (response.content).decode("utf-8")
              self.assertEquals(resp_json, '"No recommended items"')

        def test_valid_delete_recommendations(self):
                data = {"recommended_items":"8,6,7,9,","item_id":4}
                response = self.client.post(reverse('create_recommendations'), data)
                deleteresponse = self.client.post(reverse('delete_recommendations'), data)
                resp_json = (deleteresponse.content).decode("utf-8")
                self.assertEquals(resp_json, '"Successfully deleted the recommended items"')
                #duplicate deletes
                deleteresponse2 = self.client.post(reverse('delete_recommendations'), data)
                resp2_json = (deleteresponse2.content).decode("utf-8")
                self.assertEquals(resp2_json, '"No recommended items"')

            
        def tearDown(self):
            pass #nothing to tear down


        

