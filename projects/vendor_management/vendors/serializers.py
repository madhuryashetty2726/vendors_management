# serializers.py
from rest_framework import generics
from rest_framework import serializers
from .models import Vendor, VendorPerformance
from .models import PurchaseOrder
from .models import HistoricalPerformance


class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorPerformance
        fields = ['on_time_delivery_rate', 'quality_rating_avg']

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'