from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting database population...'))
        
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        
        # Create Teams
        self.stdout.write('Creating teams...')
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='Earth\'s Mightiest Heroes',
        )
        
        team_dc = Team.objects.create(
            name='Team DC',
            description='Justice League Assemble',
        )
        
        # Create Users (Superheroes)
        self.stdout.write('Creating superhero users...')
        marvel_heroes = [
            {'name': 'Iron Man', 'username': 'ironman', 'email': 'tony.stark@avengers.com'},
            {'name': 'Captain America', 'username': 'captamerica', 'email': 'steve.rogers@avengers.com'},
            {'name': 'Thor', 'username': 'thor', 'email': 'thor.odinson@asgard.com'},
            {'name': 'Black Widow', 'username': 'blackwidow', 'email': 'natasha.romanoff@avengers.com'},
            {'name': 'Hulk', 'username': 'hulk', 'email': 'bruce.banner@avengers.com'},
            {'name': 'Spider-Man', 'username': 'spiderman', 'email': 'peter.parker@avengers.com'},
        ]
        
        dc_heroes = [
            {'name': 'Superman', 'username': 'superman', 'email': 'clark.kent@dailyplanet.com'},
            {'name': 'Batman', 'username': 'batman', 'email': 'bruce.wayne@wayneenterprises.com'},
            {'name': 'Wonder Woman', 'username': 'wonderwoman', 'email': 'diana.prince@themyscira.com'},
            {'name': 'The Flash', 'username': 'theflash', 'email': 'barry.allen@ccpd.com'},
            {'name': 'Aquaman', 'username': 'aquaman', 'email': 'arthur.curry@atlantis.com'},
            {'name': 'Green Lantern', 'username': 'greenlantern', 'email': 'hal.jordan@greenlantern.com'},
        ]
        
        marvel_users = []
        for hero in marvel_heroes:
            user = User.objects.create(
                name=hero['name'],
                username=hero['username'],
                email=hero['email'],
                team_id=str(team_marvel._id),
            )
            marvel_users.append(user)
        
        dc_users = []
        for hero in dc_heroes:
            user = User.objects.create(
                name=hero['name'],
                username=hero['username'],
                email=hero['email'],
                team_id=str(team_dc._id),
            )
            dc_users.append(user)
        
        all_users = marvel_users + dc_users
        
        # Create Activities
        self.stdout.write('Creating activities...')
        activity_types = ['Running', 'Weightlifting', 'Cycling', 'Swimming', 'Boxing', 'Yoga', 'CrossFit', 'HIIT']
        
        for user in all_users:
            # Create 5-10 activities per user
            for _ in range(random.randint(5, 10)):
                activity_type = random.choice(activity_types)
                duration = random.randint(20, 120)
                calories = duration * random.randint(5, 10)
                days_ago = random.randint(0, 30)
                
                Activity.objects.create(
                    user_id=str(user._id),
                    activity_type=activity_type,
                    duration=duration,
                    calories=calories,
                    date=datetime.now().date() - timedelta(days=days_ago),
                )
        
        # Create Workouts
        self.stdout.write('Creating workout suggestions...')
        workouts = [
            {
                'name': 'Superhero Strength Training',
                'description': 'Build strength like Thor! Includes compound lifts and power exercises.',
                'difficulty': 'Advanced',
                'estimated_calories': 500,
                'duration': 60,
                'category': 'Strength',
            },
            {
                'name': 'Speed Force Cardio',
                'description': 'Run like The Flash! High-intensity interval training for speed and endurance.',
                'difficulty': 'Intermediate',
                'estimated_calories': 600,
                'duration': 45,
                'category': 'Cardio',
            },
            {
                'name': 'Web-Slinger Flexibility',
                'description': 'Flexibility training inspired by Spider-Man\'s acrobatic abilities.',
                'difficulty': 'Beginner',
                'estimated_calories': 200,
                'duration': 30,
                'category': 'Flexibility',
            },
            {
                'name': 'Hulk Smash HIIT',
                'description': 'Explosive power training with high-intensity bursts. Maximum effort!',
                'difficulty': 'Advanced',
                'estimated_calories': 700,
                'duration': 40,
                'category': 'HIIT',
            },
            {
                'name': 'Amazonian Warrior Training',
                'description': 'Combat-inspired workout combining strength and agility like Wonder Woman.',
                'difficulty': 'Advanced',
                'estimated_calories': 550,
                'duration': 50,
                'category': 'Mixed',
            },
            {
                'name': 'Bat-Core Workout',
                'description': 'Core strengthening routine for stability and balance, Batman style.',
                'difficulty': 'Intermediate',
                'estimated_calories': 300,
                'duration': 30,
                'category': 'Core',
            },
            {
                'name': 'Atlantean Swim Training',
                'description': 'Aquatic workout for full-body conditioning like Aquaman.',
                'difficulty': 'Intermediate',
                'estimated_calories': 450,
                'duration': 45,
                'category': 'Swimming',
            },
            {
                'name': 'Arc Reactor Recovery',
                'description': 'Low-impact recovery workout focusing on mobility and stretching.',
                'difficulty': 'Beginner',
                'estimated_calories': 150,
                'duration': 25,
                'category': 'Recovery',
            },
        ]
        
        for workout_data in workouts:
            Workout.objects.create(**workout_data)
        
        # Create Leaderboard entries
        self.stdout.write('Creating leaderboard entries...')
        for user in all_users:
            # Calculate user's total stats
            user_activities = Activity.objects.filter(user_id=str(user._id))
            total_calories = sum(activity.calories for activity in user_activities)
            total_activities = user_activities.count()
            
            team = team_marvel if user in marvel_users else team_dc
            
            Leaderboard.objects.create(
                user_id=str(user._id),
                user_name=user.name,
                team_id=str(team._id),
                team_name=team.name,
                total_calories=total_calories,
                total_activities=total_activities,
                rank=0,  # Will calculate ranks next
            )
        
        # Update ranks based on total calories
        leaderboard_entries = Leaderboard.objects.all().order_by('-total_calories')
        for rank, entry in enumerate(leaderboard_entries, start=1):
            entry.rank = rank
            entry.save()
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n=== Database Population Complete ==='))
        self.stdout.write(self.style.SUCCESS(f'Teams created: {Team.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Users created: {User.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Activities created: {Activity.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Workouts created: {Workout.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Leaderboard entries: {Leaderboard.objects.count()}'))
        self.stdout.write(self.style.SUCCESS('\nTop 3 Heroes:'))
        for entry in leaderboard_entries[:3]:
            self.stdout.write(self.style.SUCCESS(
                f'  {entry.rank}. {entry.user_name} ({entry.team_name}) - '
                f'{entry.total_calories} calories, {entry.total_activities} activities'
            ))
