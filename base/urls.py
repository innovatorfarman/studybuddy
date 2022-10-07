from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('<int:pk>/',views.room, name='room'),
    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<str:pk>', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>',views.deleteMessage, name="delete-message"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('user-profile/<str:pk>',views.userProfile, name='user-profile'),
    path('update-profile',views.updateProfile, name='update-profile'),
    path('topics', views.topics, name="topics"),
    path('activity', views.activity, name="activity"),
]

