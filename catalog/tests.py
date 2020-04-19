from django.test import TestCase, client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.management import call_command
from io import StringIO
from .models import Product, Category, UserFavorite

# Create your tests here.

class IndexPageTestCase(TestCase):

    def test_index_returns_200(self):
        response = self.client.get(reverse('catalog:index'))
        self.assertEqual(response.status_code, 200)



class DataTests(TestCase):

	def setUp(self):
		pizzas = Category.objects.create(name='pizzas')

		Product.objects.create(name='Pizza',
        					category=pizzas,
                            brand='casino',
                            nutrition_grade='a',                            
                            picture='www.pizzajpeg.com',
        					nutrition_image='www.pizzanutrigrade.com',
                            url='www.pizza.com')


	def test_search_returns_200(self):
		Pizza = str('Pizza')
		response = self.client.get(reverse('catalog:search'), {
			'query': Pizza,
		})
		self.assertEqual(response.status_code, 200)

	def test_search_page_redirect_302(self):
		Pizza = str('invalid name')
		response = self.client.get(reverse('catalog:search'), {
			'query': Pizza,
		})
		self.assertEqual(response.status_code, 302)


# class CommandTestCase(TestCase):


#         out = StringIO()
#         call_command('init_db', stdout=out)
#         self.assertIn('', out.getvalue())