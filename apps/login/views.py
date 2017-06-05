# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from .models import UserDB

def index(request):
    return render(request, 'login/index.html')

def login(request):
    if request.method == "POST":
        credentials = {
            'email': request.POST['email'],
            'password': request.POST['password'],
        }
        print 'Checking credentials'
        valid = UserDB.objects.login(credentials)
        print valid
        if valid[0]:
            print 'credentials verified'
            user = valid[1]
            request.session['user'] = {
                'email': user.email,
                'name': user.name,
            }
            return redirect('trips:home')
        else:
            print 'Somethings wrong'
            # create error messages
            messages.error(request, valid[1], extra_tags=valid[2])
            return redirect('/')
    return redirect('/')

def register(request):
    if request.method == "POST":
        registration = {
            'name' : request.POST['name'],
            'username' : request.POST['username'],
            'email' : request.POST['email'],
            'password' : request.POST['password'],
            'c_password' : request.POST['c_password'],
        }
        validation = UserDB.objects.validate(registration)
        if validation[0]:
            request.session['user'] = {
                'email': validation[1].email,
                'name': validation[1].name,
            }
            print "name assigned to session"
            return redirect('trips:home')
        else:
            for each in validation[1]:
                messages.error(request, each[1], extra_tags=each[2])
            return redirect('/')
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')
