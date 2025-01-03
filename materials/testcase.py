from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Material, Order, StockReport, MaterialPriceHistory
from django.core.files.uploadedfile import SimpleUploadedFile
import csv
import io


class MaterialViewSetTests(APITestCase):
    def setUp(self):
        self.material = Material.objects.create(
            name="Material 1",
            category="Category 1",
            unit="kg",
            base_price=100,
            stock=50,
            version="1.0",
        )
        self.client = APIClient()

    def test_bulk_import(self):
        """Test bulk import of materials."""
        csv_content = "name,category,unit,base_price,stock,version\nMaterial 2,Category 2,litre,200,30,1.0"
        file = SimpleUploadedFile(
            "materials.csv", csv_content.encode("utf-8"), content_type="text/csv"
        )
        response = self.client.post(reverse("material-bulk-import"), {"file": file})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Material.objects.filter(name="Material 2").exists())

    def test_bulk_export(self):
        """Test bulk export of materials."""
        response = self.client.get(reverse("material-bulk-export"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "text/csv")

    def test_stock_reports(self):
        """Test stock reports view."""
        response = self.client.get(reverse("material-stock-reports"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [{"name": "Material 1", "stock": 50}])

    def test_usage_trends(self):
        """Test usage trends."""
        response = self.client.get(reverse("material-usage-trends"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [{"name": "Material 1", "total_usage": None}])


class OrderViewSetTests(APITestCase):
    def setUp(self):
        self.material = Material.objects.create(
            name="Material 1",
            category="Category 1",
            unit="kg",
            base_price=100,
            stock=50,
            version="1.0",
        )
        self.order = Order.objects.create(
            material=self.material, status="Pending", quantity=10
        )
        self.client = APIClient()

    def test_mark_as_completed(self):
        """Test marking an order as completed."""
        response = self.client.post(
            reverse("order-mark-as-completed", kwargs={"pk": self.order.id})
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.order.status = "Processing"
        self.order.save()
        response = self.client.post(
            reverse("order-mark-as-completed", kwargs={"pk": self.order.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mark_as_processing(self):
        """Test marking an order as processing."""
        response = self.client.post(
            reverse("order-mark-as-processing", kwargs={"pk": self.order.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class StockReportViewTests(APITestCase):
    def setUp(self):
        self.stock_report = StockReport.objects.create(
            date="2024-01-01",
            report_file=SimpleUploadedFile("report.csv", b"test data"),
        )

    def test_get_stock_report(self):
        """Test retrieving stock reports."""
        response = self.client.get(reverse("stockreport-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]["date"], "2024-01-01")


class MaterialUsageTrendViewTests(APITestCase):
    def setUp(self):
        self.material = Material.objects.create(
            name="Material 1",
            category="Category 1",
            unit="kg",
            base_price=100,
            stock=50,
            version="1.0",
        )

    def test_get_material_usage_trend(self):
        """Test retrieving usage trends for a material."""
        response = self.client.get(
            reverse("material-usage-trend", kwargs={"material_id": self.material.id})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.json()["message"], "No usage data found for this material."
        )


class MaterialPriceTrendViewTests(APITestCase):
    def setUp(self):
        self.material = Material.objects.create(
            name="Material 1",
            category="Category 1",
            unit="kg",
            base_price=100,
            stock=50,
            version="1.0",
        )
        MaterialPriceHistory.objects.create(
            material=self.material, price=90, date="2023-12-31"
        )

    def test_get_material_price_trend(self):
        """Test retrieving price trends for a material."""
        response = self.client.get(
            reverse("material-price-trend", kwargs={"material_id": self.material.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["price_trend"]), 1)
