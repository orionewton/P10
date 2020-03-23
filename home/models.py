from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Food(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    img = models.TextField()
    category = models.TextField()
    stores = models.TextField()
    nutriscore = models.CharField(max_length=1)
    novascore = models.CharField(max_length=1)

    def __str__(self):
        return self.name

class Substitute(models.Model):
    urloriginal = models.ForeignKey('Food', on_delete=models.CASCADE,
                                    related_name='original')
    urlsubstitute = models.ForeignKey('Food', on_delete=models.CASCADE,
                                    related_name='substitute')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.urlsubstitute.name
