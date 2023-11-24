from django.urls import path,include
from .views import VendorListCreateView
from .views import index
from .views import VendorListCreateView, VendorDetailsView, VendorPerformanceView, AcknowledgePurchaseOrderView
from .views import PurchaseOrderListCreateView, PurchaseOrderDetailsView
from .views import HistoricalPerformanceListCreateView, HistoricalPerformanceDetailsView

urlpatterns = [
    path('', index, name='index'),
    path('vendors/', VendorListCreateView.as_view(), name='vendor-list-create'),
     path('api-auth/', include('rest_framework.urls')),
    path('api/vendors/', VendorListCreateView.as_view(), name='vendor-list-create'),
    path('api/vendors/<str:vendor_code>/', VendorDetailsView.as_view(), name='vendor-details'),
    path('api/vendors/<str:vendor_code>/performance/', VendorPerformanceView.as_view(), name='vendor-performance'),
    path('api/purchase_orders/', PurchaseOrderListCreateView.as_view(), name='purchase-order-list-create'),
    path('api/purchase_orders/<str:po_number>/', PurchaseOrderDetailsView.as_view(), name='purchase-order-details'),
    path('api/historical_performances/', HistoricalPerformanceListCreateView.as_view(), name='historical-performance-list-create'),
    path('api/historical_performances/<int:id>/', HistoricalPerformanceDetailsView.as_view(), name='historical-performance-details'),
     path('api/vendors/<str:vendor_code>/performance/', VendorPerformanceView.as_view(), name='vendor-performance'),
    path('api/purchase_orders/<str:po_number>/acknowledge/', AcknowledgePurchaseOrderView.as_view(), name='acknowledge-purchase-order'),
]
