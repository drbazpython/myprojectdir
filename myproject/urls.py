from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('myapp:spot_list'), name='home'),
    path('admin/', admin.site.urls),
    path('myapp/', include('myapp.urls')),
    path('login/', auth_views.LoginView.as_view(next_page='myapp:spot_list'), name='login'),
]




