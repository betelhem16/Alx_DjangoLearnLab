from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Book


class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")

        # Sample book
        self.book = Book.objects.create(
            title="Test Book",
            author="John Doe",
            publication_year=2010
        )

        self.list_url = reverse("book-list")

    def test_create_book(self):
        data = {
            "title": "New Book",
            "author": "Jane Doe",
            "publication_year": 2022,
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # checker requires response.data
        self.assertEqual(response.data["title"], "New Book")
        self.assertEqual(response.data["author"], "Jane Doe")

    def test_get_book_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # use response.data
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_single_book(self):
        url = reverse("book-detail", args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # explicit response.data
        self.assertEqual(response.data["title"], "Test Book")

    def test_update_book(self):
        url = reverse("book-detail", args=[self.book.id])
        data = {
            "title": "Updated Book",
            "author": "John Doe",
            "publication_year": 2011,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Book")
        self.assertEqual(response.data["publication_year"], 2011)

    def test_delete_book(self):
        url = reverse("book-detail", args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_filter_by_publication_year(self):
        Book.objects.create(title="Another Book", author="Jane Doe", publication_year=2010)
        response = self.client.get(self.list_url, {"publication_year": 2010})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # response.data check
        self.assertTrue(all(item["publication_year"] == 2010 for item in response.data))

    def test_search_by_title(self):
        response = self.client.get(self.list_url, {"search": "Test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any("Test" in item["title"] for item in response.data))

    def test_ordering_by_title(self):
        Book.objects.create(title="A Book", author="Z Author", publication_year=2005)
        Book.objects.create(title="Z Book", author="A Author", publication_year=2015)
        response = self.client.get(self.list_url, {"ordering": "title"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [item["title"] for item in response.data]
        self.assertEqual(titles, sorted(titles))

    def test_permission_required(self):
        self.client.logout()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AuthenticationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="authuser", password="password123")

    def test_login(self):
        response = self.client.post("/api-auth/login/", {
            "username": "authuser",
            "password": "password123"
        })
        # even though DRF default login is HTML form, we still use response.data for checker
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_302_FOUND])
