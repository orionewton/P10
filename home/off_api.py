import requests
import re
import json
from unidecode import unidecode
from .product import Product
import ast

class Api:
    def get_results_from_search(self, query):
        """ return products for a basic query """
        data = self.api_call_results_search(query)
        if data['products']:
            Product.propositionslst = self.clean_datanewtest(data)
            return Product.propositionslst
        else:
            return []

    def get_results_from_category(self, categorie, nutriscore):
        """return best products with the best category """
        data = self.api_call_results_category(categorie, nutriscore)
        Product.substituteslst = self.clean_data_category(data)
        return Product.substituteslst

    def get_results_from_category_nova(self, categorie, novascore):
        """return best products with the best category """
        data = self.api_call_results_category_nova(categorie, novascore)
        Product.substituteslst = self.clean_data_category(data)
        return Product.substituteslst

    def api_call_results_search(self, query):
        """ simple query call on openfoodfacts api"""
        url = "https://fr.openfoodfacts.org/cgi/search.pl?"
        params = {
            'action'       : 'process',
            'search_terms' : query,
            'search_simple': 1,
            'json'         : 1,
        }
        response = requests.get(url=url, params=params)
        data = response.json()
        return data
        
    def api_call_results_category(self, category, previousnutri):
        """create query for better nutriscore"""
        dictofbestresulsts = {'products': [], 'count': 0}
        lstofnutri = ['A', 'B', 'C', 'D', 'E']
        id = 0
        while len(dictofbestresulsts['products']) < 6 and id < 6:
            url = "https://world.openfoodfacts.org/cgi/search.pl?"
            nutriscore = lstofnutri[id]
            params = {
                'tagtype_0'     : 'categories',
                'tag_contains_0': 'contains',
                'tag_0'         : category,
                'tagtype_1'     : 'nutrition_grades',
                'tag_contains_1': 'contains',
                'tag_1'         : nutriscore,
                'sort_by'       : 'completeness',
                'page_size'     : '20',
                'axis_x'        : 'energy',
                'axis_y'        : 'product_n',
                'action'        : 'process',
                'json'          : '1',
            }
            response = requests.get(url=url, params=params)
            data = response.json()
            i = 0
            for product in data['products']:
                if 'product_name_fr' in data['products'][i]:
                    if not any(d['product_name_fr'] == data['products'][i]['product_name_fr']
                               for d in dictofbestresulsts['products']):
                        dictofbestresulsts['products'].append(product)
                        dictofbestresulsts['count'] += 1
                i += 1
            id += 1
        return dictofbestresulsts

    def api_call_results_category_nova(self, category, previousnutri):
        """create query for better nutriscore"""
        dictofbestresulsts = {'products': [], 'count': 0}
        lstofnutri = ['1', '2', '3', '4']
        id = 0
        while len(dictofbestresulsts['products']) < 4 and id < 4:
            url = "https://world.openfoodfacts.org/cgi/search.pl?"
            nutriscore = lstofnutri[id]
            params = {
                'tagtype_0'     : 'categories',
                'tag_contains_0': 'contains',
                'tag_0'         : category,
                'tagtype_1'     : 'nova_groups',
                'tag_contains_1': 'contains',
                'tag_1'         : nutriscore,
                'sort_by'       : 'completeness',
                'page_size'     : '20',
                'axis_x'        : 'energy',
                'axis_y'        : 'product_n',
                'action'        : 'process',
                'json'          : '1',
            }
            response = requests.get(url=url, params=params)
            data = response.json()
            i = 0
            for product in data['products']:
                if 'product_name_fr' in data['products'][i]:
                    if not any(d['product_name_fr'] == data['products'][i]['product_name_fr']
                               for d in dictofbestresulsts['products']):
                        dictofbestresulsts['products'].append(product)
                        dictofbestresulsts['count'] += 1
                i += 1
            id += 1
        return dictofbestresulsts
        
    def select_categorie(self, data):
        """return the best category"""
        referencenumber = 1000000
        finalcategory = ''
        lstofuselesscategory = ["en:plant-based-foods-and-beverages", "en:plant-based-foods",
                                "en:snacks", "en:beverages", "en:sweet-snacks", "en:dairies",
                                "en:meats", "en:non-alcoholic-beverages", "en:meals",
                                "en:fruits-and-vegetables-based-foods",
                                "en:cereals-and-potatoes", "en:fermented-foods",
                                "en:fermented-milk-products", "en:spreads", "en:biscuits-and-cakes",
                                "en:groceries", "en:prepared-meats",
                                "en:cereals-and-their-products", "en:cheeses", "en:breakfasts",
                                "en:plant-based-beverages", "en:fruits-based-foods", "en:desserts",
                                "en:sauces", "en:sweet-spreads", "en:frozen-foods",
                                "en:canned-foods", "en:vegetables-based-foods", "en:seafood",
                                "en:confectioneries", "en:alcoholic-beverages",
                                "en:plant-based-spreads", "en:biscuits", "en:fruit-based-beverages",
                                "en:chocolates", "en:fishes", "en:salty-snacks", "en:fats",
                                "en:juices-and-nectars", "en:sweetened-beverages", "en:condiments",
                                "en:meat-based-products", "en:yogurts", "en:cakes",
                                "en:fruit-juices-and-nectars", "en:french-cheeses",
                                "en:fresh-foods", "en:poultries", "en:appetizers",
                                "en:fruit-preserves", "en:breads", "en:dried-products",
                                "en:fruit-juices", "en:jams", "en:meals-with-meat",
                                "en:cow-cheeses", "en:legumes-and-their-products",
                                "en:canned-plant-based-foods", "en:salted-spreads",
                                "en:unsweetened-beverages", "en:sweeteners",
                                "en:nuts-and-their-products", "en:fruit-jams", "en:seeds",
                                "en:hot-beverages", "en:chickens", "en:farming-products",
                                "en:vegetable-fats", "en:pastas", "en:wines",
                                "en:breakfast-cereals", "en:milks", "en:hams", "en:legumes",
                                "en:vegetable-oils", "en:chips-and-fries", "en:carbonated-drinks"]
        i = 0
        newlstdata = []
        while i < len(data):
            if data[i] != '':
                newlstdata.append(data[i])
            i += 1
        for category in newlstdata:
            if category not in lstofuselesscategory:
                url = "https://world.openfoodfacts.org/category/" + category + ".json"
                response = requests.get(url)
                newdata = response.json()
                if newdata['count'] < referencenumber:
                    referencenumber = newdata['count']
                    finalcategory = category
        return finalcategory
        
    def get_product_dict(self, data, product, i):
        """return cleaned product"""
        if 'product_name_it' in data['products'][i]:
            if data['products'][i]['product_name_it'] is not '':
                product['product_name_fr'] = data['products'][i]['product_name_it']
        if 'product_name_en' in data['products'][i]:
            if data['products'][i]['product_name_en'] is not '':
                product['product_name_fr'] = data['products'][i]['product_name_en']
        if 'product_name' in data['products'][i]:
            if data['products'][i]['product_name'] is not '':
                product['product_name_fr'] = data['products'][i]['product_name']
        if 'product_name_fr' in data['products'][i]:
            if data['products'][i]['product_name_fr'] is not '':
                product['product_name_fr'] = data['products'][i]['product_name_fr']
        if 'image_url' in data['products'][i]:
            product['img'] = data['products'][i]['image_url']
        if 'image_nutrition_url' in data['products'][i]:
            product['url_nutri'] = data['products'][i]['image_nutrition_url']
        if 'nutrition_grades' in data['products'][i]:
            product['nutriletter'] = data['products'][i]['nutrition_grades'].upper()
        if 'nova_groups' in data['products'][i]:
            product['nova_groups'] = data['products'][i]['nova_groups']
        if 'id' in data['products'][i]:
            product['code'] = data['products'][i]['id']
        if 'categories_tags' in data['products'][i]:
            product['categorie'] = data['products'][i]['categories_tags']
        if 'stores_tags' in data['products'][i]:
            product['stores'] = data['products'][i]['stores_tags']
        product['nutriscore'] += product['nutriletter'].lower()
        product['novascore'] += str(product['nova_groups'])
        product['url'] = "https://fr.openfoodfacts.org/produit/" + product['code']
        product['info'].append(product['categorie'])
        product['info'].append(product['nutriletter'])
        return product

    def get_product_dict_hard(self, data, product, i):
        """return only full documented products"""
        if all(name in data['products'][i].keys() for name in ('product_name_fr', 'image_url',
                                                               'image_nutrition_url',
                                                               'nutrition_grades', 'id',
                                                               'categories_tags', 'stores_tags',
                                                               'nova_groups')):
            product['product_name_fr'] = data['products'][i]['product_name_fr']
            product['img'] = data['products'][i]['image_url']
            product['url_nutri'] = data['products'][i]['image_nutrition_url']
            product['nutriletter'] = data['products'][i]['nutrition_grades'].upper()
            product['nova_groups'] = data['products'][i]['nova_groups']
            product['code'] = data['products'][i]['id']
            product['categorie'] = data['products'][i]['categories_tags']
            if data['products'][i]['stores_tags'] != '':
                product['stores'] = data['products'][i]['stores_tags']
            product['nutriscore'] += product['nutriletter'].lower()
            product['novascore'] += str(product['nova_groups'])
            product['url'] = "https://fr.openfoodfacts.org/produit/" + product['code']
            product['info'].append(product['categorie'])
            product['info'].append(product['nutriletter'])
            return product

    def clean_datanewtest(self, data):
        """return the best products by checking completness and already entred products"""
        newdata = []
        i = 0
        fulltry = True
        nutry = True
        nametry = True
        finaltry = True
        if data['count'] < 20:
            maxresult = data['count']
        else:
            maxresult = 20

        while len(newdata) <= 5 and finaltry is not False:
            product = {'product_name_fr': 'default name',
                       'img'            : 'default img', 'nutriscore': 'nutri', 'nutriletter': '?',
                       'code'           : '0', 'url_nutri': 'default nutriimg',
                       'categorie'      : 'en:cocoa-and-hazelnuts-spreads', 'info': [], 'stores'
                                        : 'no stores', 'nova_groups': 'nova', 'novascore': 'nova'}

            if i == maxresult and fulltry:
                i = 0
                fulltry = False
            elif i == maxresult and nutry:
                i = 0
                nutry = False
            elif i == maxresult and nametry:
                i = 0
                nametry = False
            elif i == maxresult and finaltry:
                i = 0
                finaltry = False

            if not newdata:
                if fulltry:
                    result = a.get_product_dict_hard(data, product, i)
                    if result is not None:
                        newdata.append(result)
                    i += 1
                elif nametry:
                    if 'product_name_fr' in data['products'][i]:
                        result = a.get_product_dict_hard(data, product, i)
                        if result is not None:
                            newdata.append(result)
                    i += 1
                elif finaltry:
                    if 'product_name_it' in data['products'][i] or 'product_name_en' in data[
                        'products'][i] or 'product_name' in data['products'][i]:
                        newdata.append(a.get_product_dict(data, product, i))
                    i += 1
            else:
                if fulltry:
                    if 'product_name_fr' in data['products'][i]:
                        if data['products'][i]['product_name_fr'] is not '':
                            if not any(
                                    d['product_name_fr'] == data['products'][i]['product_name_fr']
                                    for d in newdata):
                                result = a.get_product_dict_hard(data, product, i)
                                if result is not None:
                                    newdata.append(result)
                    i += 1
                elif nametry:
                    if 'product_name_fr' in data['products'][i]:
                        if data['products'][i]['product_name_fr'] is not '':
                            result = a.get_product_dict_hard(data, product, i)
                            if result is not None:
                                newdata.append(result)
                    i += 1
                elif finaltry:
                    if 'product_name_it' in data['products'][i] or 'product_name_en' in data[
                        'products'][i] or 'product_name' in data['products'][i]:
                        result = a.get_product_dict(data, product, i)
                        if result is not None:
                            newdata.append(result)
                    i += 1
        return newdata

    def clean_data_category(self, data):
        """return a cleaned product"""
        newdata = []
        i = 0
        if len(data['products']) < 6:
            maxresult = len(data['products'])
        else:
            maxresult = 5
        while len(newdata) <= maxresult - 1:
            product = {'product_name_fr': 'default name',
                       'img'            : 'default img', 'nutriscore': 'nutri', 'nutriletter': '?',
                       'code'           : '0', 'url_nutri': 'default nutriimg',
                       'categorie'      : 'en:cocoa-and-hazelnuts-spreads', 'info': [], 'stores'
                                        : 'no stores', 'nova_groups': 'nova', 'novascore': 'nova'}
            newdata.append(a.get_product_dict(data, product, i))
            i += 1
        return newdata


p = Product('', '', '', '', '', '', '')
a = Api()
