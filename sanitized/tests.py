import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestSanitizedInputAPIView:
    """Test the SanitizedInputAPIView."""

    @pytest.fixture
    def api_client(self):
        """Create an API client."""
        return APIClient()

    def test_sanitized_input(self, api_client):
        """Test with a sanitized input."""
        url = reverse('sanitized:sanitized_input_v1')

        # Test with a sanitized input
        data = {'input': 'safe_input'}
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['result'] == 'sanitized'

    def test_unsanitized_input(self, api_client):
        """Test with an unsanitized input."""
        url = reverse('sanitized:sanitized_input_v1')

        # Test with an unsanitized input
        data = {'input': 'unsafe_input; DROP TABLE users;'}
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['result'] == 'unsanitized'

    def test_missing_input(self, api_client):
        """Test with missing input."""
        url = reverse('sanitized:sanitized_input_v1')

        # Test with missing input
        response = api_client.post(url, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['result'] == 'sanitized'

    def test_sql_injection_attempt(self, api_client):
        """Test with a SQL injection attempt."""
        url = reverse('sanitized:sanitized_input_v1')

        # Test with a SQL injection attempt
        user_input = "'; DROP TABLE users; --"
        data = {'input': user_input}
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['result'] == 'unsanitized'

    def test_union_based_sql_injection(self, api_client):
        """Test with a Union-based SQL injection attempt."""
        url = reverse('sanitized:sanitized_input_v1')

        # Test with a Union-based SQL injection attempt
        user_input = "1 UNION SELECT username, password FROM users --"
        data = {'input': user_input}
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['result'] == 'unsanitized'

    def test_boolean_based_sql_injection(self, api_client):
        """Test with a Boolean-based Blind SQL injection attempt."""
        url = reverse('sanitized:sanitized_input_v1')

        # Test with a Boolean-based Blind SQL injection attempt
        user_input = "admin' AND 1=1 --"
        data = {'input': user_input}
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['result'] == 'unsanitized'

    def test_time_based_sql_injection(self, api_client):
        """Test with a Time-based Blind SQL injection attempt."""
        url = reverse('sanitized:sanitized_input_v1')

        # Test with a Time-based Blind SQL injection attempt
        user_input = "admin' AND IF(1=1, SLEEP(5), 0) --"
        data = {'input': user_input}
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['result'] == 'unsanitized'

    def test_xss_attempt(self, api_client):
        """Test with a Cross-Site Scripting (XSS) attempt."""
        url = reverse('sanitized:sanitized_input_v1')

        # Test with a Cross-Site Scripting (XSS) attempt
        user_input = "<script>alert('XSS');</script>"
        data = {'input': user_input}
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['result'] == 'unsanitized'

    def test_sanitized_input_numbers(self, api_client):
        """Test that input containing only numbers is sanitized."""
        url = reverse('sanitized:sanitized_input_v1')

        # Test with a sanitized input containing only numbers
        user_input = "12345"
        data = {'input': user_input}
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['result'] == 'sanitized'

    def test_sanitized_input_characters(self, api_client):
        """Test that input containing only characters is sanitized."""
        url = reverse('sanitized:sanitized_input_v1')

        # Test with a sanitized input containing only characters
        user_input = "abcde"
        data = {'input': user_input}
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['result'] == 'sanitized'

    def test_sanitized_input_numbers_and_characters(self, api_client):
        """Test that input containing only numbers and characters is sanitized."""
        url = reverse('sanitized:sanitized_input_v1')
        user_input = "a1b2c3"
        data = {'input': user_input}
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['result'] == 'sanitized'

    def test_unsanitized_input_special_characters(self, api_client):
        """Test with an unsanitized input containing special characters."""
        url = reverse('sanitized:sanitized_input_v1')

        # Test with an unsanitized input containing special characters
        user_input = "!@#$%^&*"
        data = {'input': user_input}
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['result'] == 'unsanitized'

    def test_unsanitized_input_numbers_and_special_characters(self, api_client):
        """Test with an unsanitized input containing numbers and special characters."""
        url = reverse('sanitized:sanitized_input_v1')
        user_input = "123!@#"
        data = {'input': user_input}
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['result'] == 'unsanitized'
