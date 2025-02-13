from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from .models import EmailOTP, State, City

User = get_user_model()


class AccountTests(APITestCase):
    def setUp(self):
        self.generate_otp_url = "/accounts/generate_otp/"
        self.verify_otp_url = "/accounts/verify_otp/"
        self.register_url = "/accounts/"
        self.login_url = "/accounts/login/"
        self.logout_url = "/accounts/logout/"
        self.refresh_token_url = "/accounts/refresh_token/"
        self.protected_url = "/accounts/"

        self.valid_email = "test@example.com"
        self.existing_email = "existing@example.com"
        self.invalid_email = "invalid@example.com"
        self.correct_otp = None  # Will be set later
        self.wrong_format_otp = "11"
        self.wrong_otp = "9999"
        self.valid_phone_number = "+919348758478"
        self.state = State.objects.create(name="Gujarat")
        self.city = City.objects.create(name="Vadodara", state=self.state)

        # Create a user with an existing email
        self.user = User.objects.create_user(
            email=self.existing_email,
            password="SecurePass123",
            phone_number=self.valid_phone_number,
            full_name="Existing in Test",
            gender="Male",
            date_of_birth="2002-02-01",
            current_state=self.state,
            current_city=self.city,
        )

    def test_generate_otp(self):
        """Tests OTP generation for new and existing emails."""
        # Generate OTP for a new email
        response = self.client.post(self.generate_otp_url, {"email": self.valid_email})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Save OTP for later verification
        self.correct_otp = EmailOTP.objects.first().otp

        # Try generating OTP for the same email again (should still succeed)
        response = self.client.post(self.generate_otp_url, {"email": self.valid_email})
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

        # Try generating OTP for an already registered email
        response = self.client.post(
            self.generate_otp_url, {"email": self.existing_email}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verify_otp(self):
        """Tests OTP verification with incorrect details."""
        # Generate OTP for a new email
        response = self.client.post(self.generate_otp_url, {"email": self.valid_email})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Save OTP for later verification
        self.correct_otp = EmailOTP.objects.first().otp

        # Verify OTP with an email that never generated an OTP
        response = self.client.post(
            self.verify_otp_url, {"email": self.invalid_email, "otp": self.correct_otp}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Verify OTP with the correct email but incorrect OTP
        response = self.client.post(
            self.verify_otp_url, {"email": self.valid_email, "otp": self.wrong_otp}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Verify OTP with the correct email but incorrect OTP
        response = self.client.post(
            self.verify_otp_url,
            {"email": self.valid_email, "otp": self.wrong_format_otp},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Verify OTP with correct email & correct OTP
        response = self.client.post(
            self.verify_otp_url, {"email": self.valid_email, "otp": self.correct_otp}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_account(self):
        """Tests account registration with invalid and valid inputs."""

        # Successful account creation
        response = self.client.post(
            self.register_url,
            {
                "email": self.valid_email,
                "password": "SecurePass123",
                "phone_number": self.valid_phone_number,
                "father_name": "father",
                "full_name": "Registration Test",
                "gender": "Male",
                "date_of_birth": "2002-02-01",
                "current_state": "Gujarat",
                "current_city": str(self.city.name),
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Generate OTP for a new email
        response = self.client.post(self.generate_otp_url, {"email": self.valid_email})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Save OTP for later verification
        self.correct_otp = EmailOTP.objects.first().otp

        # Verify OTP with correct email & correct OTP
        response = self.client.post(
            self.verify_otp_url, {"email": self.valid_email, "otp": self.correct_otp}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Attempt registration with a password shorter than 8 characters
        response = self.client.post(
            self.register_url,
            {
                "email": self.valid_email,
                "password": "1234567",  # Too short
                "phone_number": self.valid_phone_number,
                "father_name": "father",
                "full_name": "Registration Test",
                "gender": "Male",
                "date_of_birth": "2002-02-01",
                "current_state": "Gujarat",
                "current_city": str(self.city.name),
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Attempt registration with an invalid phone_number number
        response = self.client.post(
            self.register_url,
            {
                "email": self.valid_email,
                "password": "SecurePass123",
                "phone_number": "123",  # Invalid phone_number
                "full_name": "Registration Test",
                "gender": "Male",
                "father_name": "father",
                "date_of_birth": "2002-02-01",
                "current_state": "Gujarat",
                "current_city": str(self.city.name),
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Successful account creation
        response = self.client.post(
            self.register_url,
            {
                "email": self.valid_email,
                "password": "SecurePass123",
                "phone_number": self.valid_phone_number,
                "father_name": "father",
                "full_name": "Registration Test",
                "gender": "Male",
                "date_of_birth": "2002-02-01",
                "current_state": "Gujarat",
                "current_city": str(self.city.name),
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)

    def test_logout_and_login(self):
        """Tests logout and login with correct & incorrect credentials."""

        # Attempt login with correct credentials
        response = self.client.post(
            self.login_url, {"email": self.existing_email, "password": "SecurePass123"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)

        # Save tokens for later use
        self.access_token = response.data["access_token"]
        self.refresh_token = response.data["refresh_token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        # Logout using refresh token
        response = self.client.post(
            self.logout_url, {"refresh_token": self.refresh_token}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Attempt login with incorrect credentials
        response = self.client.post(
            self.login_url, {"email": self.existing_email, "password": "WrongPass123"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Attempt login with correct credentials
        response = self.client.post(
            self.login_url, {"email": self.existing_email, "password": "SecurePass123"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)

    def test_refresh_token(self):
        # 1. Login and get tokens
        response = self.client.post(
            self.login_url, {"email": self.existing_email, "password": "SecurePass123"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)

        old_refresh_token = response.data["refresh_token"]
        self.client.cookies.clear()

        response = self.client.post(
            self.refresh_token_url, {"refresh": old_refresh_token}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

        new_refresh_token = response.data["refresh"]

        self.client.cookies.clear()
        response = self.client.post(
            self.refresh_token_url, {"refresh": str(old_refresh_token)}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(self.refresh_token_url, {"refresh": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(
            self.refresh_token_url, {"refresh": str(new_refresh_token)}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
