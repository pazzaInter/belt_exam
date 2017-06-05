from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('apps.login.urls', namespace='login')),
    url(r'^travels/', include('apps.trips.urls', namespace='trips')),
]
