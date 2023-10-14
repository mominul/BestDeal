from django.contrib import admin
from django.urls import path
from authentication.views import login_page, logout_page, signup_view
from home.views import home
from chatbot.views import chat_home, chat_clear

urlpatterns = [
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('signup/', signup_view, name='signup'),
    path('admin/', admin.site.urls),
    path('', home),
    path('chat/', chat_home, name='chat_home'),
    path('chat/clear', chat_clear, name="clear_chat"),

    #path('result/', filter_items, name='result')
]
