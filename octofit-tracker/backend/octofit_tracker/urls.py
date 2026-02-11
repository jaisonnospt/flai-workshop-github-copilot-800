"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/

GitHub Codespaces URL format: https://<codespace-name>-8000.app.github.dev
"""
import os
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .views import (
    UserViewSet, TeamViewSet, ActivityViewSet,
    LeaderboardViewSet, WorkoutViewSet
)


@api_view(['GET'])
def api_root(request, format=None):
    """
    API root view that returns URLs for all endpoints.
    Uses CODESPACE_NAME environment variable for GitHub Codespaces.
    """
    codespace_name = os.environ.get('CODESPACE_NAME')
    
    if codespace_name:
        # GitHub Codespaces URL
        base_url = f'https://{codespace_name}-8000.app.github.dev/api'
    else:
        # Local development
        base_url = request.build_absolute_uri('/api')
    
    return Response({
        'users': f'{base_url}/users/',
        'teams': f'{base_url}/teams/',
        'activities': f'{base_url}/activities/',
        'leaderboard': f'{base_url}/leaderboard/',
        'workouts': f'{base_url}/workouts/',
    })


# Create a router and register our viewsets
router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'leaderboard', LeaderboardViewSet, basename='leaderboard')
router.register(r'workouts', WorkoutViewSet, basename='workout')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_root),
    path('api/', include(router.urls)),
]
