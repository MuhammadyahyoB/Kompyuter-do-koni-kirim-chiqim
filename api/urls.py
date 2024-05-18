from django.urls import path
from . import views

urlpatterns = [
    # -------------- category list creatae detail ----------------
    path('category/listcreate/', views.CategoryList.as_view()),
    path('category/detail/<int:id>/', views.CategoryDetail.as_view()),

    # -------------- product list creatae detail ----------------
    path('product/listcreate/', views.ProductList.as_view()),
    path('product/detail/<int:id>/', views.ProductDetail.as_view()),

    # -------------- out list creatae detail ----------------
    path('out/listcreate/', views.OutList.as_view()),
    path('out/detail/<int:id>/', views.OutDetail.as_view()),

    # -------------- enter list creatae detail ----------------
    path('enter/listcreate/', views.Enterlist.as_view()),
    path('enter/detail/<int:id>/', views.EnterDetail.as_view()),

]
