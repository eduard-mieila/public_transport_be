from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Route, Station, Trip, Driver, Vehicle, Subscription, RouteStation
from .serializers import RouteSerializer, RoutePostSerializer, StationSerializer, TripGetSerializer, TripSetSerializer, DriverGetSerializer, DriverSetSerializer, VehicleSerializer, SubscriptionSerializer, UserSerializer, RouteStationSerializer
from django.contrib.auth.models import Group, User

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

# ViewSet for Route
class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    # serializer_class = RouteSerializer
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return RoutePostSerializer
        return RouteSerializer

# ViewSet for Station
class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer

# ViewSet for Trip
class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return TripSetSerializer
        return TripGetSerializer

# ViewSet for Driver
class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return DriverSetSerializer
        return DriverGetSerializer

# ViewSet for Vehicle
class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

# ViewSet for Subscription
class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

# ViewSet for Subscription
class RouteStationViewSet(viewsets.ModelViewSet):
    queryset = RouteStation.objects.all()
    serializer_class = RouteStationSerializer
# Create your views here.
