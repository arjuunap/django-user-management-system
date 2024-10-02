from django.urls import path
from . import views
urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_login/',views.admin_login,name='admin_login'),
    path('admin_panel/',views.admin_panel,name='admin_panel'),
    path('add_user',views.add_user,name='add_user'),
    path('delete/<int:id>',views.delete,name='delete'),
    path('update/<int:id>',views.update,name='update'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),
    path('test/',views.test,name='test')
    
]
