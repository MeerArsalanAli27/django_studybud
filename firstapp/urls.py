from django.urls import path
from . import views

urlpatterns = [
 path("", views.home, name="home"),
 path("myname/",views.myname,name="myname"),
 path("room/",views.room,name="room1"),

 path('room/<str:pk>/',views.showoneroom,name="showoneroom"),

 path("createroom/",views.createroom,name="createroom"),
 path('updateroom/<str:pk>/',views.updateroom,name="update-room"),

  path('deleteroom/<str:pk>/',views.deleteroom,name="delete-room"),


 path('deletemessage/<str:pk>/',views.deletemessage,name="deletemessage"), 
 path('loginform/',views.loginform,name="loginform"),

 path('logoutt',views.logoutuser,name="logoutuser"),

 
 path('registeruser/',views.registeruser,name="registeruser"),

path('userprofile/<str:pk>/',views.userprofile,name="userprofile"),
      


  
     
]