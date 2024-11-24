from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'myapp'

urlpatterns = [
    path('', views.spot_list, name='spot_list'),
    path('spot/<int:pk>/', views.spot_detail, name='spot_detail'),
    path('spot/<int:pk>/add_review/', views.add_review, name='add_review'),
    path('spot/<int:pk>/add_condition/', views.add_condition, name='add_condition'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
	path('about/', views.about,name='about')
]

