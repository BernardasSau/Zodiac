from django.contrib.auth import views as auth_views
from . import views
from django.urls import path, include, reverse_lazy


urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.user_list, name='users-all'),
    path('matchmaking/', views.matchmaking, name='matchmaking'),
    path('contact/', views.contact, name='contact'),
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile_view, name='edit-profile'),
    path('comments/', views.comments_view, name='comments'),
    path('profile-detail/<int:user_id>/', views.profile_detail, name='profile-detail'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('index')), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('thank-you/', views.thank_you_view, name='thank_you'),
    path('compatible-users/', views.compatible_users, name='compatible_users'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('generate-natal-chart/', views.generate_natal_chart, name='generate_natal_chart'),
]
