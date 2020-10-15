from django.db import models

class ChosenColors(models.Model):
    huemin = models.IntegerField()
    satmin = models.IntegerField()
    valmin = models.IntegerField()
    huemax = models.IntegerField()
    satmax = models.IntegerField()
    valmax = models.IntegerField()
    B = models.IntegerField()
    G = models.IntegerField()
    R = models.IntegerField()