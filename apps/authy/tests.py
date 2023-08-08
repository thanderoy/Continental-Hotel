from django.test import TestCase
from django.contrib.auth import get_user_model


class AuthyTests(TestCase):
    def test_create_superuser(self):
        db = get_user_model()

        # Happy Case
        su = db.objects.create_superuser(
            "testsu@authy.com", "username", "first_name", "last_name", "str0ngP@SSW0RD"
        )
        self.assertEqual(su.email, "testsu@authy.com")
        self.assertEqual(su.username, "username")
        self.assertEqual(su.first_name, "first_name")
        self.assertTrue(su.is_superuser)
        self.assertTrue(su.is_staff)
        self.assertTrue(su.is_active)
        self.assertEqual(str(su), "username")

    def test_create_user(self):
        db = get_user_model()

        # Happy Case
        u = db.objects.create_superuser(
            "test@authy.com", "username", "first_name", "last_name", "str0ngP@SSW0RD"
        )
        self.assertEqual(u.email, "testsu@authy.com")
        self.assertEqual(u.username, "username")
        self.assertEqual(u.first_name, "first_name")
        self.assertFalse(u.is_superuser)
        self.assertFalse(u.is_staff)
        self.assertFalse(u.is_active)
        self.assertEqual(str(u), "username")
