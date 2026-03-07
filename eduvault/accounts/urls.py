from django.urls import path
from .views import login_view
from .views import logout_user
urlpatterns = [
    path('', login_view, name='login'),
path('logout/', logout_user, name='logout')
]