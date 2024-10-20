from django.contrib import admin
from .models import Station, Route, Trip, Vehicle, Ticket, Subscription, Driver, UserProfile

# Register your models here.
admin.site.register(Station)
admin.site.register(Route)
admin.site.register(Trip)
admin.site.register(Vehicle)
admin.site.register(Ticket)
admin.site.register(Subscription)
admin.site.register(Driver)
admin.site.register(UserProfile)