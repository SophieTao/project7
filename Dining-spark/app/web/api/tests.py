from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import unittest

		
class HomeTest(unittest.TestCase):

	def setUp(self):
		self.driver = webdriver.Chrome()
		self.driver.get("http://localhost:8003/home/")
		self.driver.implicitly_wait(5)

	def test_home_title(self):
		self.assertIn("Cav Dining", self.driver.title)
		meal_link = self.driver.find_element_by_id("meals")
		meal_link.click()

	def tearDown(self):
		self.driver.quit()


class OtherPagesTest(unittest.TestCase):

	def setUp(self):
		self.driver = webdriver.Chrome()
		
		self.driver.implicitly_wait(10)

	def test_login(self):
		# Sign up
		self.driver.get("http://localhost:8003/create_account/")
		susrname = self.driver.find_element_by_id("username")
		semail = self.driver.find_element_by_id("email")
		spsw = self.driver.find_element_by_id("password")
		susrname.send_keys("zona")
		semail.send_keys("z@gmail.com")
		spsw.send_keys("z")
		ssubmit_button = self.driver.find_element_by_id("submit_button")
		ssubmit_button.submit()

		# Log in
		self.driver.get("http://localhost:8003/login/")
		usrname = self.driver.find_element_by_id("username")
		psw = self.driver.find_element_by_id("password")
		usrname.send_keys("zona")
		psw.send_keys("z")
		submit_button = self.driver.find_element_by_id("submit_button")
		submit_button.submit()


		# Create meals
		self.driver.get("http://localhost:8003/create_listing/")
		mealname = self.driver.find_element_by_id("mealname")
		description = self.driver.find_element_by_id("description")
		location = self.driver.find_element_by_id("location")
		date = self.driver.find_element_by_id("date")
		calorie = self.driver.find_element_by_id("Calories")

		mealname.send_keys("toast")
		description.send_keys("yummy")
		location.send_keys("Runk")
		date.send_keys("1/1/2017")
		calorie.send_keys("80")

		submit_button = self.driver.find_element_by_id("submit_button")
		submit_button.submit()



	def tearDown(self):
		self.driver.quit()


if __name__ == '__main__':
	unittest.main()