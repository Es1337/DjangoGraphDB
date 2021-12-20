from django.urls import path
from . import views

urlpatterns = [
    path('people/', views.person),
    path('people/<str:uid>', views.person_detail),
    path('trophies/', views.trophy),
    path('trophies/<str:uid>', views.trophy_detail),
    path('leagues/', views.league),
    path('leagues/<str:uid>', views.league_detail),
    path('clubs/', views.club),
    path('clubs/<str:uid>', views.club_detail),
    path('players/', views.player),
    path('players/<str:uid>', views.player_detail),
    path('managers/', views.manager),
    path('managers/<str:uid>', views.manager_detail),
    path('connect/', views.connect),
    # path('midfield/', views.midfielders),
    # path('attack/', views.forwards)
]