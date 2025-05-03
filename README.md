# Project Setup Guide

This guide will help you set up and run both the backend (Flask) and frontend (Vue + Vite) parts of this project.

---

## Prerequisites

-  **Python 3.8+** (for backend)
-  **Node.js 18+** and **npm** or **pnpm** (for frontend)
-  (Optional) **PostgreSQL** if you want to use a production database instead of SQLite

---

## Backend Setup (Flask)

1. **Create a virtual environment (recommended):**

   ```sh
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

   > **Note:** If you see an error about `pg_config` missing when installing `psycopg2`, you can either:
   >
   > -  Install PostgreSQL and ensure `pg_config` is in your PATH, **or**
   > -  Replace `psycopg2` with `psycopg2-binary` in `requirements.txt` for easier installation (not recommended for production).

3. **Configure environment variables:**

   Create a `.env` file in the root directory (same place as `requirements.txt`). Example:

   ```
   SECRET_KEY=your-secret-key
   JWT_SECRET_KEY=your-jwt-secret-key
   DATABASE_URL=sqlite:///app.db
   ```

   -  If you want to use PostgreSQL, set `DATABASE_URL` like:
      ```
      DATABASE_URL=postgresql://username:password@localhost/dbname
      ```

4. **Run database migrations (if needed):**

   ```sh
   flask db upgrade
   ```

5. **Start the backend server:**

   ```sh
   python run.py
   ```

   The backend will be available at `http://localhost:5000`.

---

## Frontend Setup (Vue + Vite)

1. **Navigate to the frontend directory:**

   ```sh
   cd frontend
   ```

2. **Install dependencies:**

   ```sh
   pnpm install
   # or, if you don't have pnpm:
   npm install
   ```

3. **Start the frontend development server:**

   ```sh
   pnpm run dev
   # or
   npm run dev
   ```

   The frontend will be available at the address shown in your terminal (usually `http://localhost:5173`).

---

## Additional Notes

-  **Code Quality:** This project enforces error handling, logging, and code formatting. Please follow the conventions in the codebase.
-  **Environment Variables:** Never commit secrets or production credentials to version control.
-  **For more details on frontend development, see** `frontend/README.md`.

---

## Troubleshooting

-  If you have issues with dependencies, ensure your Python and Node.js versions match the prerequisites.
-  For database errors, check your `.env` configuration and ensure the database server is running (if using PostgreSQL).
-  For `psycopg2` installation issues, see the note above or use `psycopg2-binary` for local development.

---

Happy coding!
