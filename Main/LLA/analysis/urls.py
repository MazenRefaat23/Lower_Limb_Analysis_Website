from django.urls import path

from . import views

urlpatterns = [
    path('<int:id>/', views.person, name="person"),

]