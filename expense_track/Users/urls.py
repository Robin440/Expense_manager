from django.contrib import admin
from django.urls import path
from Users import views

urlpatterns = [
    path('',views.landing_page,name='landing_page'),
    path('user_login',views.user_login,name='user_login_page'),
    path('user_registration',views.user_registration,name='user_registration_page'),
    path('home',views.home,name='home_page'),
    path('logout',views.logout,name='logout_user'),
    path('new_expenses',views.new_expenses,name='add_expenses'),
    path('edit_expense/<int:expense_id>/', views.edit_expense, name='edit_expense'),
    path('filter_expenses_by_date/', views.filter_expenses_by_date, name='filter_expenses_by_date'),
    path('search_expenses/', views.search_expenses, name='search_expenses'),
    path('delete_expense/<int:expense_id>/', views.delete_expense, name='delete_expenses'),
]
