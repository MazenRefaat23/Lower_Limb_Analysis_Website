from django.db import models

# Create your models here.


class peaple(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    height = models.IntegerField()
    weight = models.IntegerField()

    def __str__(self):
        return f"{self.name}: age = {self.age}, height = {self.height}, weight = {self.weight}"
