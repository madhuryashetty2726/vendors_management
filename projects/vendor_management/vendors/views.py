from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import Vendor, VendorPerformance
from .serializers import VendorSerializer, VendorPerformanceSerializer
from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer
from .models import HistoricalPerformance
from .serializers import HistoricalPerformanceSerializer
from django.db.models import Count, Avg
from django.utils import timezone

# Create your views here.

class VendorDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_field = 'vendor_code'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Retrieve and attach performance metrics
        performance_instance, created = VendorPerformance.objects.get_or_create(vendor=instance)
        performance_serializer = VendorPerformanceSerializer(performance_instance)

        response_data = serializer.data
        response_data['performance'] = performance_serializer.data

        return Response(response_data)
    
class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_field = 'vendor_code'

class VendorPerformanceView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_field = 'vendor_code'

    def perform_on_time_delivery_calculation(self, vendor):
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        total_completed_pos = completed_pos.count()

        on_time_deliveries = completed_pos.filter(delivery_date__lte=timezone.now())
        on_time_delivery_rate = on_time_deliveries.count() / total_completed_pos if total_completed_pos > 0 else 0.0

        vendor.on_time_delivery_rate = on_time_delivery_rate
        vendor.save()

    def perform_quality_rating_avg_calculation(self, vendor):
        completed_pos_with_ratings = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False)
        quality_rating_avg = completed_pos_with_ratings.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0.0

        vendor.quality_rating_avg = quality_rating_avg
        vendor.save()

    def perform_average_response_time_calculation(self, vendor):
        acknowledged_pos = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
        response_times = acknowledged_pos.values_list('acknowledgment_date', 'issue_date')

        average_response_time = sum([(ack_date - issue_date).total_seconds() for ack_date, issue_date in response_times]) / len(response_times) if len(response_times) > 0 else 0.0

        vendor.average_response_time = average_response_time
        vendor.save()

    def perform_fulfillment_rate_calculation(self, vendor):
        total_pos = PurchaseOrder.objects.filter(vendor=vendor)
        total_po_count = total_pos.count()

        fulfilled_pos = total_pos.filter(status='completed', issues__isnull=True)
        fulfilled_po_count = fulfilled_pos.count()

        fulfillment_rate = fulfilled_po_count / total_po_count if total_po_count > 0 else 0.0

        vendor.fulfillment_rate = fulfillment_rate
        vendor.save()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Calculate and update performance metrics
        self.perform_on_time_delivery_calculation(instance)
        self.perform_quality_rating_avg_calculation(instance)
        self.perform_average_response_time_calculation(instance)
        self.perform_fulfillment_rate_calculation(instance)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AcknowledgePurchaseOrderView(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_field = 'po_number'

    def perform_update(self, serializer):
        # Update acknowledgment_date
        serializer.save(acknowledgment_date=timezone.now())

        # Recalculate average_response_time for the vendor
        vendor = serializer.instance.vendor
        view = VendorPerformanceView()
        view.perform_average_response_time_calculation(vendor)


def index(request):
    return render(request, 'index.html')

class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_field = 'po_number'



class HistoricalPerformanceListCreateView(generics.ListCreateAPIView):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer

class HistoricalPerformanceDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer
    lookup_field = 'id'

