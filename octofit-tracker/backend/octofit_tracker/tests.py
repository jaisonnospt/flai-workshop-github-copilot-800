from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import datetime, timedelta
from .models import User, Team, Activity, Leaderboard, Workout


class TeamModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(
            name='Test Team',
            description='Test Description'
        )
    
    def test_team_creation(self):
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.description, 'Test Description')
        self.assertIsNotNone(self.team._id)
    
    def test_team_str(self):
        self.assertEqual(str(self.team), 'Test Team')


class UserModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name='Test Team')
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            team_id=str(self.team._id)
        )
    
    def test_user_creation(self):
        self.assertEqual(self.user.name, 'Test User')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertIsNotNone(self.user._id)
    
    def test_user_str(self):
        self.assertEqual(str(self.user), 'Test User')


class ActivityModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name='Test Team')
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            team_id=str(self.team._id)
        )
        self.activity = Activity.objects.create(
            user_id=str(self.user._id),
            activity_type='Running',
            duration=30,
            calories=300,
            date=datetime.now().date()
        )
    
    def test_activity_creation(self):
        self.assertEqual(self.activity.activity_type, 'Running')
        self.assertEqual(self.activity.duration, 30)
        self.assertEqual(self.activity.calories, 300)


class TeamAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.team = Team.objects.create(
            name='Test Team',
            description='Test Description'
        )
    
    def test_get_teams_list(self):
        response = self.client.get('/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_team_detail(self):
        response = self.client.get(f'/teams/{self.team._id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Team')
    
    def test_create_team(self):
        data = {
            'name': 'New Team',
            'description': 'New Description'
        }
        response = self.client.post('/teams/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 2)


class UserAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.team = Team.objects.create(name='Test Team')
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            team_id=str(self.team._id)
        )
    
    def test_get_users_list(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_user_detail(self):
        response = self.client.get(f'/users/{self.user._id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test User')
    
    def test_create_user(self):
        data = {
            'name': 'New User',
            'email': 'new@example.com',
            'team_id': str(self.team._id)
        }
        response = self.client.post('/users/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)


class ActivityAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.team = Team.objects.create(name='Test Team')
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            team_id=str(self.team._id)
        )
        self.activity = Activity.objects.create(
            user_id=str(self.user._id),
            activity_type='Running',
            duration=30,
            calories=300,
            date=datetime.now().date()
        )
    
    def test_get_activities_list(self):
        response = self.client.get('/activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_activity(self):
        data = {
            'user_id': str(self.user._id),
            'activity_type': 'Cycling',
            'duration': 45,
            'calories': 400,
            'date': datetime.now().date().isoformat()
        }
        response = self.client.post('/activities/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 2)


class LeaderboardAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.team = Team.objects.create(name='Test Team')
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            team_id=str(self.team._id)
        )
        self.leaderboard = Leaderboard.objects.create(
            user_id=str(self.user._id),
            user_name=self.user.name,
            team_id=str(self.team._id),
            team_name=self.team.name,
            total_calories=1000,
            total_activities=10,
            rank=1
        )
    
    def test_get_leaderboard_list(self):
        response = self.client.get('/leaderboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_top_leaderboard(self):
        response = self.client.get('/leaderboard/top/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WorkoutAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.workout = Workout.objects.create(
            name='Test Workout',
            description='Test Description',
            difficulty='Intermediate',
            estimated_calories=500,
            duration=60,
            category='Strength'
        )
    
    def test_get_workouts_list(self):
        response = self.client.get('/workouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_workout_detail(self):
        response = self.client.get(f'/workouts/{self.workout._id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Workout')
    
    def test_filter_by_difficulty(self):
        response = self.client.get('/workouts/by_difficulty/?level=Intermediate')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
