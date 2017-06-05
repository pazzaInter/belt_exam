# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Trip, UserDB

def index(request):
    if 'user' in request.session:
        print 'Joined trip', Trip.objects.get(id=1).users_joined.all()
        current_user = UserDB.objects.get(email=request.session['user']['email'])
        trips = Trip.objects.all()
        context = {
            'my_trips': trips.filter(planned_by=current_user).order_by('start_date'),
            'trips': trips.exclude(planned_by=current_user).exclude(users_joined=current_user),
            'joined': UserDB.objects.get(email=current_user.email).joined_trips.all(),
        }
        return render(request, 'trips/index.html', context)
    return redirect('login:index')

def trip(request):
    if 'user' in request.session:
        return render(request, 'trips/add.html')
    return redirect('login:index')

def destination(request, id):
    if 'user' in request.session:
        trip = Trip.objects.get(id=id)
        context = {
            'trip': trip,
            'users_joined': trip.users_joined.all()
        }
        return render(request, 'trips/destination.html', context)
    return redirect('login:index')

def add_trip(request):
    if request.method == 'POST':
        trip_info = {
            'destination': request.POST['destination'],
            'plan': request.POST['plan'],
            'start_date': request.POST['start_date'],
            'end_date': request.POST['end_date'],
            'user_email': request.session['user']['email'],
        }
        print request.session['user']['email']
        print 'Checking trip info is valid'
        valid = Trip.objects.check_add(trip_info)
        print valid
        if valid[0]:
            print 'trip info accepted and added'
            return redirect('trips:home')
        else:
            print 'Somethings wrong'
            # create error messages
            for each in valid[1]:
                messages.error(request, each[0], extra_tags=each[1])
            return redirect('trips:trip')
    return redirect('login:index')

def join(request, id):
    Trip.objects.join_trip(id, request.session['user']['email'])
    print 'Joined trip'
    return redirect('trips:home')
