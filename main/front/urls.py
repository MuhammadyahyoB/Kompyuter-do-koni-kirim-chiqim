from django.urls import path
from . import views



urlpatterns = [
    path('', views.index , name='index'),

    # --------- log-in log-out ------------------------
    path('login/',views.log_in, name='login'),
    path('logout/',views.log_out, name='logout'),
    path('error/',views.error, name='error'),

    # ----------- category - list , create, delete, update ------------------------
    path('category/list/',views.category_list, name='category_list'),
    path('category/create/',views.category_create, name='category_create'),
    path('category/delete/<str:code>/',views.category_delete, name='category_delete'),
    path('category/update/<str:code>/',views.category_update, name='category_update'),

    # ----------- Product - list , create, update, delete ------------------------
    path('product/list/',views.product_list, name='product_list'),
    path('product/create/',views.product_create, name='product_create'),
    path('product/update/<str:code>/',views.product_update, name='product_update'),
    path('product/delete/<str:code>/',views.product_delete, name='product_delete'),

    # ----------- Enter - list, update, create ------------------------------
    path('enter/list/',views.enter_list, name='enter_list'),
    path('enter/create/',views.enter_create, name='enter_create'),
    path('enter/update/<int:id>/',views.enter_update, name='enter_update'),

    # ----------- Out - list create update ---------------------------
    path('out/list/',views.out_list, name='out_list'),
    path('out/create/',views.out_create, name='out_create'),
    path('out/update/<int:id>/',views.out_update, name='out_update'),

    # ------------- Profile --------------------------------
    path('profile/',views.profil, name='profile'),
    path('settings/',views.setting, name='settings'),

    # ------------- Return - create list -------------------
    path('return/create/',views.return_create, name='return_create'),
    path('return/list/',views.return_list, name='return_list'),
    path('return/update/<int:id>/',views.return_update, name='return_update'),
]