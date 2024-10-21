from rest_framework import serializers
from .models import Route, Station, Trip, Driver, Vehicle, Subscription, RouteStation
from django.contrib.auth.models import Group, User

# Serializer for Station
class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ['id', 'name', 'location']

# Serializer for RouteStation (to handle the ordered list of stations)
class RouteStationSerializer(serializers.ModelSerializer):
    station = serializers.PrimaryKeyRelatedField(queryset=Station.objects.all())
    route = serializers.PrimaryKeyRelatedField(queryset=Route.objects.all())
    class Meta:
        model = RouteStation
        fields = ['id', 'route', 'station', 'order', 'time_from_start'] 

class RouteStationFullStationSerializer(serializers.ModelSerializer):
    station = StationSerializer()
    # route = serializers.PrimaryKeyRelatedField(queryset=Route.objects.all())
    class Meta:
        model = RouteStation
        fields = ['id', 'station', 'order', 'time_from_start'] 

# Serializer for Route
class RouteSerializer(serializers.ModelSerializer):
    # stations = StationSerializer() // This is wrong, because stations is a list of RouteStation objects
    start_station = StationSerializer()
    end_station = StationSerializer()
    stations = RouteStationFullStationSerializer(source='routestation_set', many=True)

    class Meta:
        model = Route
        fields = ['id', 'start_station', 'end_station', 'stations']

class RoutePostSerializer(serializers.ModelSerializer):
    stations = serializers.PrimaryKeyRelatedField(queryset=Station.objects.all(), many=True, required=False)
    start_station = serializers.PrimaryKeyRelatedField(queryset=Station.objects.all(), required=True)
    end_station = serializers.PrimaryKeyRelatedField(queryset=Station.objects.all(), required=True)

    class Meta:
        model = Route
        fields = ['id', 'start_station', 'end_station', 'stations']

class RouteIDSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = ['id']



# Serializer for Vehicle
class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# Serializer for Driver
class DriverSetSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField()  # To display the user info
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    class Meta:
        model = Driver
        fields = ['id', 'full_name', 'hire_date', 'license_number', 'user']


class DriverGetSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField()  # To display the user info
    user = UserSerializer()
    class Meta:
        model = Driver
        fields = ['id', 'full_name', 'hire_date', 'license_number', 'user']

# Serializer for Trip
class TripGetSerializer(serializers.ModelSerializer):
    route = RouteSerializer()
    driver = DriverGetSerializer()
    vehicle = VehicleSerializer()
    current_station = StationSerializer()

    class Meta:
        model = Trip
        fields = ['id', 'route', 'vehicle', 'driver', 'start_time', 'end_time', 'current_station', 'status']

class TripSetSerializer(serializers.ModelSerializer):
    route = serializers.PrimaryKeyRelatedField(queryset=Route.objects.all(), required=True)
    driver = serializers.PrimaryKeyRelatedField(queryset=Driver.objects.all(), required=True)
    vehicle = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all(), required=True)
    current_station = serializers.PrimaryKeyRelatedField(queryset=Station.objects.all(), required=False)
    start_time = serializers.DateTimeField(required=False)
    end_time = serializers.DateTimeField(required=False)
    status = serializers.CharField(required=False, default='Scheduled')
    class Meta:
        model = Trip
        fields = ['id', 'route', 'vehicle', 'driver', 'start_time', 'end_time','current_station', 'status']

# Serializer for Subscription
class SubscriptionSerializer(serializers.ModelSerializer):
    traveler = serializers.StringRelatedField()

    class Meta:
        model = Subscription
        fields = ['id', 'traveler', 'start_date', 'end_date']

