import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db import models

class Driver(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=255)
    hire_date = models.DateField()
    license_number = models.CharField(max_length=50)

    def __str__(self):
        return self.full_name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=[('Traveler', 'Traveler'), ('Driver', 'Driver'), ('Admin', 'Admin')], null=False, default='Traveler')

    def __str__(self):
        return self.user.username


class Station(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)  # poate fi un string ce reprezintă adresa

    def __str__(self):
        return self.name

# Intermediate model for RouteStation
class RouteStation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    route = models.ForeignKey('Route', on_delete=models.CASCADE)
    order = models.PositiveIntegerField()  # Field to store the order of the station in the route
    # add a field for distance in minutes from start_station
    time_from_start = models.PositiveIntegerField(null=False, default=0)  # Field to store the distance in minutes from the start station
    class Meta:
        ordering = ['order']  # Order by the "order" field

    def __str__(self):
        return f"{self.station.name} (Order: {self.order})"

class Vehicle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    license_plate = models.CharField(max_length=7)
    capacity = models.IntegerField()
    model = models.CharField(max_length=100)

    def __str__(self):
        return self.license_plate


class Route(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_station = models.ForeignKey(Station, related_name='start_routes', on_delete=models.CASCADE)
    end_station = models.ForeignKey(Station, related_name='end_routes', on_delete=models.CASCADE)
    stations = models.ManyToManyField(Station, through=RouteStation, related_name='stations_list')
    def __str__(self):
        return f"{self.route_number}: {self.start_station.name} to {self.end_station.name}"


class Trip(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    current_station = models.ForeignKey(Station, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, choices=[('scheduled', 'Scheduled'),('in_station', 'In Station'), ('left_station', 'Left Station')])

    def __str__(self):
        return f"Trip on route {self.route.route_number} by {self.vehicle.license_plate}"


class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    traveler = models.ForeignKey(User, limit_choices_to={'role': 'Traveler'}, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Ticket for {self.traveler.username} on {self.trip.route.route_number}"
    
# Model for Subscription
class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    traveler = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'Traveler'})
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Subscription for {self.traveler.username}"