from django.urls import path
from .views import GetRoutes, NewEntry, EntryList, SingleEntry, GetEveryThing, RegisterUser
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns= [
    path('register/', RegisterUser.as_view(), name= 'register_user'),
    path('login/', TokenObtainPairView.as_view(), name= 'token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name= 'token_refresh'),

    path('get-everything/', GetEveryThing.as_view(), name= 'get_everything'),
    path('', GetRoutes.as_view(), name= 'get_url'),
    path('entry/new/', NewEntry.as_view(), name= 'new_entry'),
    path('entry/', EntryList.as_view(), name= 'entry_list'),
    path('entry/<str:pk>/', SingleEntry.as_view(), name= 'single_entry'),
]