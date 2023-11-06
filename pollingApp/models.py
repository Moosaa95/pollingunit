# polling/models.py
from django.db import models

class State(models.Model):
    name = models.CharField(max_length=50)

class LGA(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

class Ward(models.Model):
    name = models.CharField(max_length=100)
    lga = models.ForeignKey(LGA, on_delete=models.CASCADE)

class PollingUnit(models.Model):
    name = models.CharField(max_length=150)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)

class ElectionResult(models.Model):
    polling_unit = models.ForeignKey(PollingUnit, on_delete=models.CASCADE)
    party = models.CharField(max_length=50)
    score = models.IntegerField()
