class Product:
    propositionslst = []
    substituteslst = []

    def __init__(self, name, img, nutriimg, nutriletter, code, category, nutriscore):
        self.name = name
        self.img = img
        self.nutriimg = nutriimg
        self.nutriletter = nutriletter
        self.code = code
        self.url = "https://fr.openfoodfacts.org/produit/" + self.code
        self.apiurl = "https://fr.openfoodfacts.org/api/v0/produit/" + self.code
        self.category = category
        self.nutriscore = nutriscore

    def create_list(self, lst):
        newlist = []
        for i in lst:
            newprod = Product(i['name'], i['img'], i['url_nutri'],
                           i['nutriletter'], i['code'], i['categorie'],
                           i['nutriscore'])
            newlist.append(newfood)
            return newlist


