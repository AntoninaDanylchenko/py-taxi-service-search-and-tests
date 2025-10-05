from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer

DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicDriversViewTests(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriversViewTests(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="driver1",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_toggle_assign_to_car(self):
        car = Car.objects.create(
            model="X5",
            manufacturer=Manufacturer.objects.create(name="BMW")
        )
        url = reverse("taxi:toggle-car-assign", args=[car.id])
        response = self.client.get(url)
        self.assertRedirects(
            response,
            reverse("taxi:car-detail", args=[car.id])
        )
        self.assertIn(car, self.user.cars.all())
