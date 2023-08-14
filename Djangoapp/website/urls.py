from django.urls import path
from .views import homepage
from .views import info
urlpatterns = [
    path('',homepage.as_view(),name="home"),
    # path('info/<str:routeid>/<str:doj>',info.as_view(),name="info"),
]
