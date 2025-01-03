from .serializers import MaterialSerializer, OrderSerializer
import csv
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from .utils_methods import validate_order, update_inventory
from django.db.models import Sum
from django.shortcuts import get_object_or_404

from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Material, MaterialPriceHistory

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response

# Importing Models
from .models import Material, Order
from .models import StockReport, MaterialUsage, MaterialPriceHistory, Material


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    
    @action(detail=False, methods=['post'])
    def bulk_import(self, request):
        file = request.FILES['file']
        data = csv.DictReader(file.read().decode('utf-8').splitlines())
        for row in data:
            Material.objects.create(**row)
        return Response({"message": "Bulk import successful"}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def bulk_export(self, request):
        materials = Material.objects.all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="materials.csv"'
        writer = csv.writer(response)
        writer.writerow(['name', 'category', 'unit', 'base_price', 'stock', 'version'])
        for material in materials:
            writer.writerow([material.name, material.category, material.unit, material.base_price, material.stock, material.version])
        return response
    
    @action(detail=False, methods=['get'])
    def stock_reports(self, request):
        materials = Material.objects.all()
        report = [{"name": m.name, "stock": m.stock} for m in materials]
        return Response(report, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def usage_trends(self, request):
        trends = Material.objects.annotate(total_usage=Sum('orderitem__quantity'))
        report = [{"name": m.name, "total_usage": m.total_usage} for m in trends]
        return Response(report, status=status.HTTP_200_OK)
    

    @receiver(pre_save, sender=Material)
    def track_price_changes(sender, instance, **kwargs):
        if instance.pk:  # Check if the Material object already exists
            try:
                original_material = Material.objects.get(pk=instance.pk)
                if original_material.base_price != instance.base_price:
                    # Save the old price in MaterialPriceHistory
                    MaterialPriceHistory.objects.create(
                        material=instance,
                        price=original_material.base_price
                    )
            except Material.DoesNotExist:
                pass
    

    

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        # Validate order before saving
        order = serializer.save()
        try:
            validate_order(order)
            order.calculate_total_price()
        except ValidationError as e:
            order.delete()
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='complete')
    def mark_as_completed(self, request, pk=None):
        """Mark an order as completed and update inventory."""
        order = self.get_object()
        if order.status != 'Processing':
            return Response(
                {"error": "Only Processing orders can be completed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            update_inventory(order)
            order.status = 'Completed'
            order.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['post'], url_path='processing')
    def mark_as_processing(self, request, pk=None):
        """Mark an order as Processing and update inventory."""
        order = self.get_object()
        if order.status != 'Pending':
            return Response(
                {"error": "Only Pending orders can be processed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            update_inventory(order)
            order.status = 'Processing'
            order.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class StockReportView(APIView):

    def get(self, request):
        reports = StockReport.objects.all().order_by("-date")
        data = [{"date": report.date, "url": report.report_file.url} for report in reports]
        return Response(data)
    
    

class StockReportView(APIView):
    def get(self, request):
        reports = StockReport.objects.all().order_by("-date")
        data = [{"date": report.date, "url": report.report_file.url} for report in reports]
        return Response(data)

class MaterialUsageTrendView(APIView):
    def get(self, request, material_id):
        try:
            material = Material.objects.get(id=material_id)
            usage_data = (
                MaterialUsage.objects.filter(material=material)
                .values("date")
                .annotate(total_used=Sum("quantity_used"))
                .order_by("date")
            )
            if not usage_data:
                return Response(
                    {"message": "No usage data found for this material."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            return Response({"material": material.name, "trend": list(usage_data)})
        except Material.DoesNotExist:
            return Response(
                {"error": "Material not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
class MaterialPriceTrendView(APIView):
    def get(self, request, material_id):
        # Get the material or return a 404 if it doesn't exist
        material = get_object_or_404(Material, id=material_id)
        
        # Fetch price history for the material
        price_history = MaterialPriceHistory.objects.filter(material=material).order_by("date")
        
        if not price_history.exists():
            # Return a message if no price history is available
            return Response(
                {
                    "material": material.name,
                    "price_trend": [],
                    "message": "No price history available for this material."
                },
                status=status.HTTP_200_OK
            )
        
        # Prepare the price trend data
        data = [{"date": entry.date, "price": entry.price} for entry in price_history]
        return Response({"material": material.name, "price_trend": data})