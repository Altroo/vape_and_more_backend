from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class CustomUserAuthTests(TestCase):
    def test_custom_user_uses_email_as_login_identifier(self):
        user_model = get_user_model()

        self.assertEqual(user_model.__name__, "CustomUser")
        self.assertEqual(user_model.USERNAME_FIELD, "email")
        self.assertFalse(
            any(field.name == "username" for field in user_model._meta.fields)
        )

        user_model.objects.create_superuser(
            email="admin@example.com",
            password="strong-password",
        )

        self.assertTrue(
            self.client.login(email="admin@example.com", password="strong-password")
        )

    def test_admin_login_form_shows_email_label(self):
        response = self.client.get(reverse("admin:login"))

        self.assertContains(response, "Adresse e-mail")
        self.assertNotContains(response, ">Username<")
