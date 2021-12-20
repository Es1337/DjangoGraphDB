from rest_framework import serializers
from .models import Person, Trophy, League, Club, Player, Manager

class PersonSerialiser(serializers.Serializer):
    uid = serializers.CharField(read_only=True)
    name = serializers.CharField(required=False, allow_blank=True, max_length=50)
    surname = serializers.CharField(required=False, allow_blank=True, max_length=50)
    created = serializers.DateTimeField(read_only=True)

    def create(self, data):
        return Person.objects.create(**data)

    def update(self, instance, data):
        instance.name = data.get('name', instance.name)
        instance.surname = data.get('surname', instance.surname)

        instance.save()
        return instance

    class Meta:
        model = Person

class TrophySerialiser(serializers.Serializer):
    uid = serializers.CharField(read_only=True)
    name = serializers.CharField(required=False, allow_blank=True, max_length=50)
    date_won = serializers.DateField()
    created = serializers.DateTimeField(read_only=True)

    def create(self, data):
        return Trophy.objects.create(**data)

    def update(self, instance, data):
        instance.name = data.get('name', instance.name)
        instance.date_won = data.get('date_won', instance.date_won)

        instance.save()
        return instance

    class Meta:
        model = Trophy

class LeagueSerialiser(serializers.Serializer):
    uid = serializers.CharField(read_only=True)
    name = serializers.CharField(required=False, allow_blank=True, max_length=50)
    country = serializers.CharField(required=False, allow_blank=True, max_length=50)
    created = serializers.DateTimeField(read_only=True)

    def create(self, data):
        return League.objects.create(**data)

    def update(self, instance, data):
        instance.name = data.get('name', instance.name)
        instance.country = data.get('country', instance.country)

        instance.save()
        return instance

    class Meta:
        model = League

class ClubSerialiser(serializers.Serializer):
    uid = serializers.CharField(read_only=True)
    name = serializers.CharField(required=False, allow_blank=True, max_length=50)
    created = serializers.DateTimeField(read_only=True)

    def create(self, data):
        return Club.objects.create(**data)

    def update(self, instance, data):
        instance.name = data.get('name', instance.name)

        instance.save()
        return instance

    class Meta:
        model = Club

class PlayerSerialiser(serializers.Serializer):
    uid = serializers.CharField(read_only=True)
    name = serializers.CharField(required=False, allow_blank=True, max_length=50)
    surname = serializers.CharField(required=False, allow_blank=True, max_length=50)
    created = serializers.DateTimeField(read_only=True)

    def create(self, data):
        return Player.objects.create(**data)

    def update(self, instance, data):
        instance.name = data.get('name', instance.name)
        instance.surname = data.get('surname', instance.surname)

        instance.save()
        return instance

    class Meta:
        model = Player

class ManagerSerialiser(serializers.Serializer):
    uid = serializers.CharField(read_only=True)
    name = serializers.CharField(required=False, allow_blank=True, max_length=50)
    surname = serializers.CharField(required=False, allow_blank=True, max_length=50)
    created = serializers.DateTimeField(read_only=True)

    def create(self, data):
        return Manager.objects.create(**data)

    def update(self, instance, data):
        instance.name = data.get('name', instance.name)
        instance.surname = data.get('surname', instance.surname)

        instance.save()
        return instance

    class Meta:
        model = Manager