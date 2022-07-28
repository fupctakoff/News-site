from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeNews.as_view(), name='home'),
    path('category/<int:category_id>/', views.NewsByCategory.as_view(), name='category'),
    path('new/<int:new_id>/', views.GetNew.as_view(), name='new'),
    path('new/add-new/', views.CreateNew.as_view(), name='add-new'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
