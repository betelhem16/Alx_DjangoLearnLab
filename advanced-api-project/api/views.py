from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from api.models import Book


class BookAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2020,
            author=self.user
        )

    def test_create_book(self):
        data = {
            "title": "New Book",
            "publication_year": 2022,
            "author": self.user.id
        }
        response = self.client.post("/api/books/create/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("title", response.data)  # ✅ check response.data
        self.assertEqual(response.data["title"], "New Book")

    def test_list_books(self):
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)  # ✅ response.data is list
        self.assertIn("title", response.data[0])

    def test_get_single_book(self):
        response = self.client.get(f"/api/books/{self.book.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Book")

    def test_update_book(self):
        data = {
            "title": "Updated Book",
            "publication_year": 2023,
            "author": self.user.id
        }
        response = self.client.put(f"/api/books/update/{self.book.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Book")

    def test_delete_book(self):
        response = self.client.delete(f"/api/books/delete/{self.book.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_filter_books_by_title(self):
        Book.objects.create(title="Another Book", publication_year=2021, author=self.user)
        response = self.client.get("/api/books/?search=Test")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any("Test Book" in book["title"] for book in response.data))

    def test_order_books_by_year(self):
        Book.objects.create(title="Older Book", publication_year=1999, author=self.user)
        response = self.client.get("/api/books/?ordering=publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book["publication_year"] for book in response.data]
        self.assertEqual(years, sorted(years))

    def test_permissions_required(self):
        self.client.force_authenticate(user=None)  # logout
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
