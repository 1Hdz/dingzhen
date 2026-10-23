from django.urls import path
from app01 import views

urlpatterns = [
    # 部门管理
    path('depart/list/', views.depart_list),
    path('depart/add/', views.depart_add),
    path('depart/<int:aid>/delete/', views.depart_delete),
    path('depart/<int:aid>/edit/', views.depart_edit),

    # 用户管理
    path('user/list/', views.user_list),
    path('user/add/', views.user_add),
    path('user/model/form/add/', views.user_model_form_add),
    path('user/<int:uid>/edit/', views.user_edit),
    path('user/<int:uid>/delete/', views.user_delete),

    # 靓号管理
    path('pretty/list/', views.pretty_list),
    path('pretty/add/', views.pretty_add),
    path('pretty/<int:pid>/edit/', views.pretty_edit),
    path('pretty/<int:pid>/delete/', views.pretty_delete),
]
