# Zeronity: Local Development and Integration Testing

To run the project locally and verify the integration between the frontend and backend, follow these steps.

## 1. Backend Setup (Flask)

The backend is a Flask application that uses an in-memory database for this prototype.

```bash
cd back
# Install dependencies
uv sync
# Run the backend (it will start on http://localhost:5000)
uv run src/main.py
```

**Note:** CORS is enabled with `supports_credentials=True` to allow session handling from the frontend.

## 2. Frontend Setup (SvelteKit)

The frontend is a SvelteKit SPA using Gruvbox aesthetics.

```bash
cd front
# Install dependencies
pnpm install
# Run the frontend in development mode
pnpm dev
```

Open your browser to `http://localhost:5173`.

## 3. Verification Steps

1. **Sign Up / Login:** Go to the frontend and create a new account.
2. **Post a Note:** Enter text and an optional image URL (e.g., `https://picsum.photos/400/300`) to see it in the feed.
3. **Delete a Note:** Use the "Delete" button on your post.
4. **Logout:** Use the "Log Out" button to clear your session.

## 4. Automated Integration Testing (Playwright)

You can run E2E tests to verify the full flow:

```bash
cd front
# Ensure the backend is running in another terminal
pnpm test:e2e
```

Current E2E tests are located in `front/e2e/`.

## Suggestions for Further Improvement

* **Persistent Database:** Replace `InMemoryRepository` with a real database (e.g., SQLite via SQLAlchemy) for data persistence.
* **Image Uploads:** Implement actual file uploads instead of just linking to external URLs.
* **ActivityPub Integration:** Implement the actual ActivityPub protocol for federation.
