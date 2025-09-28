 Advanced API Project

## Task 2: Filtering, Searching, and Ordering

### Features Implemented
1. **Filtering**
   - Users can filter books by:
     - `title`
     - `author`
     - `publication_year`

   Example:

GET /api/books/?title=The River Between
GET /api/books/?author=1
GET /api/books/?publication_year=1965


2. **Searching**
- Users can search by title or author name.

Example:

GET /api/books/?search=River


3. **Ordering**
- Users can order results by `title` or `publication_year`.

Example:

GET /api/books/?ordering=title
GET /api/books/?ordering=-publication_year


### Permissions
- **List and Retrieve**: Open to all users (read-only access).
- **Create, Update, Delete**: Only for authenticated users.