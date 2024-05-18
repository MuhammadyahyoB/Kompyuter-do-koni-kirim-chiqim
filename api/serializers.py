from main import models

from rest_framework import serializers


# ------------------- categories  serializers ----------------
class CategorySerializer(serializers.ModelSerializer):
    """ Category serializer"""
    class Meta:
        model = models.Category
        fields = '__all__'

# -------------------- Product serializers --------------------
class ProductSerializer(serializers.ModelSerializer):
    """ Product serializer"""
    class Meta:
        model = models.Product
        fields = '__all__'

# -------------------- Enter serializers --------------------
class EnterSerializer(serializers.ModelSerializer):
    """ Enter serializer"""
    class Meta:
        model = models.Enter
        fields = '__all__'


# -------------------- Out serializers --------------------
class OutSerializer(serializers.ModelSerializer):
    """ Out serializer"""
    class Meta:
        model = models.Out
        fields = '__all__'
