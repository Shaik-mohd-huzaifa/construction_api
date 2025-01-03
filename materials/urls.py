from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MaterialViewSet, OrderViewSet, StockReportView, MaterialUsageTrendView, MaterialPriceTrendView

router = DefaultRouter()
router.register(r'materials', MaterialViewSet, basename='material')
router.register(r'orders', OrderViewSet, basename='order')


urlpatterns = [
    path('', include(router.urls)),
    path("reports/stock-levels/", StockReportView.as_view(), name="stock_report"),
    path("usage-trends/<int:material_id>/", MaterialUsageTrendView.as_view(), name="usage_trend"),
    path("price-fluctuations/<int:material_id>/", MaterialPriceTrendView.as_view(), name="price_fluctuation"),
]
