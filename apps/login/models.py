# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import re, bcrypt

EMAIL_REGEX = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
NAME_REGEX = re.compile(r'(^\b([A-Z]{1}[a-z]+) ([A-Z]{1}[a-z]+)\b$)')

class UserDBManager(models.Manager):

    def validate(self, data):
        response = []
        errors = 0

        # check name
        if NAME_REGEX.match(data['name']) and len(data['name']) > 2:
            response.append([True, '', ''])
        else:
            errors += 1
            response.append([False, 'First name must be all letters and at least 2 characters', 'name'])

        # check username
        if data['username'].isalnum() and len(data['username']) > 2:
            response.append([True, '', ''])
        else:
            errors += 1
            response.append([False, 'Alias must be only letters and numbers with at least 2 characters', 'username'])

        # check email
        if EMAIL_REGEX.match(data['email']):
            try:
                self.get(email = data['email'])
                errors += 1
                response.append([False, 'Please enter a different email', 'email'])
            except ObjectDoesNotExist:
                response.append([True, '', ''])
        else:
            errors += 1
            response.append([False, 'Must be a valid Email format', 'email'])

        # check password
        if len(data['password']) > 7:
            if data['password'] == data['c_password']:
                response.append([True, '', ''])
            else:
                errors += 1
                response.append([False, 'Passwords must match', 'c_password'])
        else:
            errors += 1
            response.append([False, 'Password must be at least 8 characters', 'password'])

        # check for any errors and return approriate message if so, no errors then just return successful message
        if errors > 0:
            return [False, response]
        else:
            new_user = UserDB(name=data['name'], username=data['username'], email=data['email'])
            hashed_pw = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
            new_user.password = hashed_pw
            new_user.save()
            return [True, new_user]

    def login(self, data):
        # first check if information entered is valid before we ping db
        if EMAIL_REGEX.match(data['email']) and len(data['password'])>7:
            # if valid then check if credentials match those stored in db
            try:
                user = self.get(email = data['email'])
                if user:
                    # if we find a matching email then check password
                    if bcrypt.checkpw(data['password'].encode(), self.get(email = data['email']).password.encode()):
                        # if all valid then return the user
                        return [True, user]
                    else:
                        return [False, 'Incorrect email or password', 'login-error']
            except:
                return [False, 'Incorrect email or password', 'login-error']
        # if info is not valid then just return error and not ping db
        else:
            return [False, 'Incorrect email or password', 'login-error']

class UserDB(models.Model):
    name = models.CharField(max_length = 100)
    username = models.CharField(max_length = 30)
    email = models.CharField(max_length = 100)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserDBManager()

    def __str__(self):
        return self.name + " " + self.username + " " + self.email
