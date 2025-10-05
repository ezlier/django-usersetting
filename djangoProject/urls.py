
from django.contrib import admin
from django.urls import path
from app01 import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('depart/list/', views.depart_list),
    path('depart/add/', views.depart_add),
    path('depart/delete/', views.depart_delete),
    path('depart/<int:nid>/edit/', views.depart_edit),

    path('user/list/', views.user_list),
    path('user/add/', views.user_add),
    path('user/<int:nid>/edit/', views.user_edit),
    path('user/<int:nid>/delete/', views.user_delete),

    path('PrettyNum/list/', views.prettynum_list),
    path('PrettyNum/add/', views.prettynum_add),
]
