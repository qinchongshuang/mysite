
from django.conf.urls import url
from user import views



urlpatterns = [
    url(r'^login$',views.user_login,name='login'),
    url(r'logout$',views.user_logout,name='logout'),
    url(r'^register$',views.user_register,name='register'),
    url(r'^delete(?P<user_id>\d*)$',views.user_delete,name='delete'),
    url(r'^edit(?P<user_id>\d*)$',views.user_edit,name='edit'),
]
