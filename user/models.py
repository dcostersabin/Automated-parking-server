from django.db import models
from django.contrib.auth.models import User


class UserDetails(models.Model):
    user_id = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    balance = models.FloatField(default=0)


class Economy(models.Model):
    hash = models.TextField(null=False, unique=True)
    value = models.IntegerField(null=False)
    validity = models.BooleanField(default=True)


class Venue(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    long = models.TextField
    lat = models.TextField
    status = models.BooleanField(default=True)
    total_agent = models.IntegerField()


class Agents(models.Model):
    id = models.TextField(primary_key=True, max_length=255)
    venue = models.ForeignKey(Venue, null=False, on_delete=models.CASCADE)
    spaceStatus = models.IntegerField()
    booked_status = models.BooleanField()
    openCloseStatus = models.BooleanField(default=False)


class Booking(models.Model):
    agent = models.ForeignKey(Agents, null=False, on_delete=models.CASCADE)
    startTime = models.CharField(null=False,max_length=255)
    endTime = models.CharField(null=False,max_length=255)
    state = models.BooleanField(default=True)
    paidStatus = models.BooleanField(default=False)
    booked_by = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    received = models.FloatField()


class Transaction(models.Model):
    type = models.CharField(max_length=255)
    amount = models.FloatField()
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
