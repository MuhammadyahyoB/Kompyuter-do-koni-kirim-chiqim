from django.shortcuts import render
from rest_framework import generics
from . import serializers
from main import models

# >>>>>>>>>> Category : list create update delete serializers <<<<<<<<<

class CategoryList(generics.ListCreateAPIView):
    """List of categories"""
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

# ------- detail -----------------------------------
class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    """Detail of a category"""
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer   
    lookup_field = 'id'


# >>>>>>>>>> Product : list create update delete serializers <<<<<<<<<

class ProductList(generics.ListCreateAPIView):
    """List of products"""
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer

# ----------------- detail ------------------------
class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    """Detail of a product"""
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    lookup_field = 'id'


# >>>>>>>>>> Out : list create update delete serializers <<<<<<<<<
    
class OutList(generics.ListCreateAPIView):
    """List of out """
    queryset = models.Out.objects.all()
    serializer_class = serializers.OutSerializer

# ----------- detail  ------------------------
class OutDetail(generics.RetrieveUpdateDestroyAPIView):
    """ Detail of a out """
    queryset = models.Out.objects.all()
    serializer_class = serializers.OutSerializer
    lookup_field = 'id'


# >>>>>>>>>> Enter : list create update delete serializers <<<<<<<<<
    
class Enterlist(generics.ListCreateAPIView):
    """ List of enter """
    queryset = models.Enter.objects.all()
    serializer_class = serializers.EnterSerializer

# ----------- detail  ------------------------
class EnterDetail(generics.RetrieveUpdateDestroyAPIView):
    """ Detail of a enter """
    queryset = models.Enter.objects.all()
    serializer_class = serializers.EnterSerializer
    lookup_field = 'id'