from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models
from octofit_tracker import models as app_models

from django.conf import settings

from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete all data from collections
        User = get_user_model()
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create users
        users = [
            User(email='ironman@marvel.com', username='ironman', team=marvel),
            User(email='captain@marvel.com', username='captain', team=marvel),
            User(email='batman@dc.com', username='batman', team=dc),
            User(email='superman@dc.com', username='superman', team=dc),
        ]
        for user in users:
            user.set_password('password')
            user.save()

        # Create activities
        activities = [
            Activity(user=users[0], type='run', duration=30, distance=5),
            Activity(user=users[1], type='cycle', duration=45, distance=15),
            Activity(user=users[2], type='swim', duration=60, distance=2),
            Activity(user=users[3], type='walk', duration=20, distance=2),
        ]
        for activity in activities:
            activity.save()

        # Create workouts
        workouts = [
            Workout(user=users[0], name='Chest Day', description='Bench press, push-ups'),
            Workout(user=users[1], name='Leg Day', description='Squats, lunges'),
            Workout(user=users[2], name='Cardio', description='Running, cycling'),
            Workout(user=users[3], name='Strength', description='Deadlifts, pull-ups'),
        ]
        for workout in workouts:
            workout.save()

        # Create leaderboard entries
        Leaderboard.objects.create(user=users[0], points=100)
        Leaderboard.objects.create(user=users[1], points=90)
        Leaderboard.objects.create(user=users[2], points=80)
        Leaderboard.objects.create(user=users[3], points=70)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
