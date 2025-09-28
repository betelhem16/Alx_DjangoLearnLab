# api/test_views.py
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from .models import Author, Book

User = get_user_model()


class BookAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create authors
        cls.author1 = Author.objects.create(name="Author One")
        cls.author2 = Author.objects.create(name="Author Two")

        # Create some books
        cls.book1 = Book.objects.create(
            title="Alpha Book", publication_year=2000, author=cls.author1
        )
        cls.book2 = Book.objects.create(
            title="Beta Book", publication_year=2010, author=cls.author2
        )
        cls.book3 = Book.objects.create(
            title="Gamma River", publication_year=2005, author=cls.author1
        )

        # Create a test user and token for authenticated endpoints
        cls.user = User.objects.create_user(username="testuser", password="testpass123")
        cls.token = Token.objects.create(user=cls.user)

        # Endpoints
        cls.list_url = reverse("book-list")           # /api/books/
        cls.create_url = reverse("book-create")       # /api/books/create/
        # detail/update/delete use pk in URL - will compute in tests

    def setUp(self):
        # new client for each test
        self.client = APIClient()

    # --- Read operations (public) ---

    def test_list_books_public(self):
        """Anyone (no auth) can list books"""
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # Ensure returned count >= created in setUpTestData
        self.assertGreaterEqual(len(resp.json()), 3)

    def test_retrieve_book_detail_public(self):
        """Anyone can retrieve a single book"""
        url = reverse("book-detail", kwargs={"pk": self.book1.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json().get("title"), "Alpha Book")

    # --- Create requires authentication ---

    def test_create_book_unauthenticated_forbidden(self):
        """Unauthenticated users cannot create"""
        payload = {"title": "New Book", "publication_year": 2020, "author": self.author1.pk}
        resp = self.client.post(self.create_url, payload, format="json")
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_create_book_authenticated(self):
        """Authenticated user can create a book"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        payload = {"title": "New Book", "publication_year": 2020, "author": self.author1.pk}
        resp = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.filter(title="New Book").exists(), True)

    # --- Update requires authentication ---

    def test_update_book_unauthenticated_forbidden(self):
        url = reverse("book-update", kwargs={"pk": self.book2.pk})
        payload = {"title": "Beta Book Updated", "publication_year": 2011, "author": self.author2.pk}
        resp = self.client.put(url, payload, format="json")
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_update_book_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        url = reverse("book-update", kwargs={"pk": self.book2.pk})
        payload = {"title": "Beta Book Updated", "publication_year": 2011, "author": self.author2.pk}
        resp = self.client.put(url, payload, format="json")
        self.assertIn(resp.status_code, (status.HTTP_200_OK, status.HTTP_202_ACCEPTED))
        self.book2.refresh_from_db()
        self.assertEqual(self.book2.title, "Beta Book Updated")
        self.assertEqual(self.book2.publication_year, 2011)

    # --- Delete requires authentication ---

    def test_delete_book_unauthenticated_forbidden(self):
        url = reverse("book-delete", kwargs={"pk": self.book3.pk})
        resp = self.client.delete(url)
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_delete_book_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        url = reverse("book-delete", kwargs={"pk": self.book3.pk})
        resp = self.client.delete(url)
        self.assertIn(resp.status_code, (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK))
        self.assertFalse(Book.objects.filter(pk=self.book3.pk).exists())

    # --- Filtering, Searching, Ordering ---

    def test_filter_by_publication_year(self):
        """Filter books by publication_year query param"""
        resp = self.client.get(self.list_url, {"publication_year": 2010})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        # All returned items should have publication_year == 2010
        self.assertTrue(all(item["publication_year"] == 2010 for item in data))

    def test_search_by_title(self):
        """Search for books matching 'River' in title"""
        resp = self.client.get(self.list_url, {"search": "River"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        # At least one returned book should contain 'River' in title (case-insensitive)
        self.assertTrue(any("river" in item["title"].lower() for item in data))

    def test_ordering_by_publication_year_desc(self):
        """Ordering - check that ordering=-publication_year returns descending years"""
        resp = self.client.get(self.list_url, {"ordering": "-publication_year"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        years = [item["publication_year"] for item in data]
        # list should be non-increasing
        self.assertEqual(years, sorted(years, reverse=True))
