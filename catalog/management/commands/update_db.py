import requests

from django.core.management.base import BaseCommand, CommandError
from django.db.utils import DataError, IntegrityError
from catalog.models import Category, Product
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseCommand):
    help = 'Update the database'

    CATEGORIES = [
        'Apéritif',
        'Snacks salés',
        'Viandes',
        'Produits à tartiner',
        'Boissons aux fruits',
        'Poissons',
        'Chocolats',
        'Pains',
        'Jambons',
        'Confiseries chocolatées',
        'Soupes'
        ]

    def up_db(self):

        for category in self.CATEGORIES:
            new_category = Category.objects.create(name=category)
            params = {
                    'action': 'process',
                    'json': 1,
                    'page_size': 200,
                    'page': 1,
                    'tagtype_0': 'categories',
                    'tag_contains_0': 'contains',
                    'tag_0': category,
                }

            response = requests.get(
                'https://fr.openfoodfacts.org/cgi/search.pl', params=params)

            data = response.json()
            products = data['products']
            for product in products:
                test = product["product_name"]
                try:
                    p = Product.objects.get(name=test)

                except ObjectDoesNotExist:
                    try:
                        name = product["product_name"]
                        brand = product["brands"]
                        nutrition_grade = product["nutrition_grades"]
                        url = product["url"]
                        picture = product['image_front_url']
                        nutrition_image = product["image_nutrition_small_url"]

                        Product.objects.create(
                            name=name,
                            category=new_category,
                            brand=brand,
                            nutrition_grade=nutrition_grade,
                            url=url,
                            picture=picture,
                            nutrition_image=nutrition_image)


                    except KeyError:
                        pass

                    except DataError:
                        pass

                    except IntegrityError:
                        pass

    def handle(self, *args, **options):
        self.up_db()
