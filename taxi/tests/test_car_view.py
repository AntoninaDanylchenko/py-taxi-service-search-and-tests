from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

CAR_LIST_URL = reverse("taxi:car-list")


class PublicCarViewTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test_123",
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="test name", country="test Country"
        )
        self.car1 = Car.objects.create(
            manufacturer=self.manufacturer,
            model="test model"
        )
        self.car2 = Car.objects.create(
            manufacturer=self.manufacturer,
            model="another model2"
        )
        self.car1.drivers.add(self.user)
        self.car2.drivers.add(self.user)

    def test_login_required(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertEqual(res.status_code, 200)

    def test_list_view_displays_cars(self):
        response = self.client.get(reverse("taxi:car-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")
        self.assertIn(self.car1, response.context["car_list"])
        self.assertIn(self.car2, response.context["car_list"])

    def test_search_filters_queryset(self):
        """
        Search form should filter cars by model.
        """
        response = self.client.get(reverse("taxi:car-list"), {"model": "test"})
        car_list = response.context["car_list"]
        self.assertIn(self.car1, car_list)
        self.assertNotIn(self.car2, car_list)

    def test_context_contains_search_form(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertIn("search_form", response.context)
        form = response.context["search_form"]
        self.assertIn("model", form.fields)

    def test_list_view_uses_correct_template(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertTemplateUsed(response, "taxi/car_list.html")
