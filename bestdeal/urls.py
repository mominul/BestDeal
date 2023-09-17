from django.contrib import admin
from django.urls import path
from authentication.views import login_page, logout_page, signup_view
from home.views import home, filter_items

urlpatterns = [
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('signup/', signup_view, name='signup'),
    path('admin/', admin.site.urls),
    path('', home),
    path('result/', filter_items, name='result')
]
