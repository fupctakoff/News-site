from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeNews.as_view(), name='home'),
    path('category/<int:category_id>/', views.NewsByCategory.as_view(), name='category'),
    path('new/<int:new_id>/', views.GetNew.as_view(), name='new'),
    path('new/add-new/', views.CreateNew.as_view(), name='add-new'),
]
