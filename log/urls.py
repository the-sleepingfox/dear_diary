from django.urls import path
from .views import EntryList, GetRoutes, SingleEntry

urlpatterns= [
    path('', GetRoutes.as_view(), name= 'get_url'),
    path('entry-list/', EntryList.as_view(), name= 'entry_list'),
    path('entry/<str:pk>/', SingleEntry.as_view(), name= 'single_entry'),
]