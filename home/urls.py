from django.urls import path

from home.views import (index_view, login_view, logout_view, register_view, user_dashboard_view)


urlpatterns = [
    path('', index_view, name='index_url'),
    path('login/', login_view, name='login_url'),
    path('logout/', logout_view, name='logout_url'),
    path('register/', register_view, name='register_url'),
    path('user-dashboard/', user_dashboard_view, name='user_dashboard_url'),
]
