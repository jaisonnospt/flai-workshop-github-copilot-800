from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Team, Activity, Leaderboard, Workout
from .serializers import (
    UserSerializer, TeamSerializer, ActivitySerializer,
    LeaderboardSerializer, WorkoutSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users (superheroes)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=True, methods=['get'])
    def activities(self, request, pk=None):
        """Get all activities for a specific user"""
        user = self.get_object()
        activities = Activity.objects.filter(user_id=str(user._id))
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)


class TeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint for teams
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Get all members of a specific team"""
        team = self.get_object()
        users = User.objects.filter(team_id=str(team._id))
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get team statistics"""
        team = self.get_object()
        users = User.objects.filter(team_id=str(team._id))
        total_members = users.count()
        
        team_leaderboard = Leaderboard.objects.filter(team_id=str(team._id))
        total_calories = sum(entry.total_calories for entry in team_leaderboard)
        total_activities = sum(entry.total_activities for entry in team_leaderboard)
        
        return Response({
            'team_name': team.name,
            'total_members': total_members,
            'total_calories': total_calories,
            'total_activities': total_activities
        })


class ActivityViewSet(viewsets.ModelViewSet):
    """
    API endpoint for activities
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent activities (last 10)"""
        activities = Activity.objects.all().order_by('-created_at')[:10]
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)


class LeaderboardViewSet(viewsets.ModelViewSet):
    """
    API endpoint for leaderboard
    """
    queryset = Leaderboard.objects.all().order_by('rank')
    serializer_class = LeaderboardSerializer
    
    @action(detail=False, methods=['get'])
    def top(self, request):
        """Get top 10 users"""
        top_users = Leaderboard.objects.all().order_by('rank')[:10]
        serializer = self.get_serializer(top_users, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_team(self, request):
        """Get leaderboard grouped by team"""
        teams = Team.objects.all()
        result = []
        
        for team in teams:
            team_entries = Leaderboard.objects.filter(team_id=str(team._id)).order_by('rank')
            result.append({
                'team_name': team.name,
                'team_id': str(team._id),
                'members': LeaderboardSerializer(team_entries, many=True).data
            })
        
        return Response(result)


class WorkoutViewSet(viewsets.ModelViewSet):
    """
    API endpoint for workout suggestions
    """
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    
    @action(detail=False, methods=['get'])
    def by_difficulty(self, request):
        """Get workouts filtered by difficulty level"""
        difficulty = request.query_params.get('level', None)
        if difficulty:
            workouts = Workout.objects.filter(difficulty__iexact=difficulty)
        else:
            workouts = Workout.objects.all()
        serializer = self.get_serializer(workouts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get workouts filtered by category"""
        category = request.query_params.get('name', None)
        if category:
            workouts = Workout.objects.filter(category__iexact=category)
        else:
            workouts = Workout.objects.all()
        serializer = self.get_serializer(workouts, many=True)
        return Response(serializer.data)
