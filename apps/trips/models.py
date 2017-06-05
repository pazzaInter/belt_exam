# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..login.models import UserDB
import datetime

class Trip_Manager(models.Manager):
    def check_add(self, data):
        errors = []
        if len(data['destination']) < 1:
            errors.append(['*required field', 'destination'])
        if len(data['plan']) < 1:
            errors.append(['*required field', 'plan'])
        if len(data['start_date']) < 10:
            errors.append(['*enter full date', 'start_date'])
        if len(data['end_date']) < 10:
            errors.append(['*enter full date', 'end_date'])
        if len(errors) > 1:
            return [False, errors]
        elif datetime.datetime.today() > datetime.datetime.strptime(data['start_date'].encode(), '%Y-%m-%d'):
            errors.append(['*start date must be after today', 'start_date'])
            return [False, errors]
        elif data['start_date'] >= data['end_date']:
            errors.append(['*end date must be after start date', 'end_date'])
            return [False, errors]
        else:
            new_trip = Trip.objects.create(destination=data['destination'], plan=data['plan'], planned_by=UserDB.objects.get(email=data['user_email']), start_date=data['start_date'], end_date=data['end_date'])
            return [True, 'trip added']

    def join_trip(self, id, email):
        user_joining = UserDB.objects.get(email=email)
        trip = Trip.objects.get(id=id)
        trip.users_joined.add(user_joining)

class Trip(models.Model):
    destination = models.CharField(max_length=30)
    plan = models.TextField()
    planned_by = models.ForeignKey(UserDB, related_name='planned_trips')
    users_joined = models.ManyToManyField(UserDB, related_name='joined_trips')
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Trip_Manager()
