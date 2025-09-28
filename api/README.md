## 📑 View Configurations

This project uses Django REST Framework’s **generic views** to implement CRUD functionality for the `Book` model.  
Below is a breakdown of each view and its purpose:

### 🔹 BookListView (`/api/books/`)
- **Class:** `ListAPIView`
- **Method(s):** `GET`
- **Purpose:** Retrieve all `Book` records from the database.
- **Permissions:** Authenticated users only (`IsAuthenticated`).

### 🔹 BookDetailView (`/api/books/<id>/`)
- **Class:** `RetrieveAPIView`
- **Method(s):** `GET`
- **Purpose:** Retrieve details of a single `Book` by its primary key (ID).
- **Permissions:** Authenticated users only.

### 🔹 BookCreateView (`/api/books/create/`)
- **Class:** `CreateAPIView`
- **Method(s):** `POST`
- **Purpose:** Add a new `Book` record to the database.
- **Permissions:** Authenticated users only.
- **Customizations:**
  - Uses serializer validation to check required fields.
  - Could be extended to automatically attach the current user.

### 🔹 BookUpdateView (`/api/books/<id>/update/`)
- **Class:** `UpdateAPIView`
- **Method(s):** `PUT`, `PATCH`
- **Purpose:** Modify details of an existing `Book`.
- **Permissions:** Authenticated users only.
- **Customizations:**
  - Serializer validation ensures correct data is provided before saving.

### 🔹 BookDeleteView (`/api/books/<id>/delete/`)
- **Class:** `DestroyAPIView`
- **Method(s):** `DELETE`
- **Purpose:** Permanently delete a `Book`.
- **Permissions:** Authenticated users only.
- **Customizations:**
  - Returns HTTP 204 (No Content) on success.

---

## ⚙️ Custom Settings

In `settings.py` we configured REST Framework as follows:

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}
