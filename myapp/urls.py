from django.urls import path
from .views import ItemListCreateView,get_route

urlpatterns = [
    path('items/', ItemListCreateView.as_view(), name='item-list-create'),
     path("get-route/", get_route, name="get_route"),
]