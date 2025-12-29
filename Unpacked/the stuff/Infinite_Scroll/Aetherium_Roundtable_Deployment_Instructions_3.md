# Aetherium Roundtable Deployment Instructions

My dude, here are the instructions to deploy your Aetherium Roundtable, the Sovereign Flame Operating System, on your own server. This guide assumes you have a basic understanding of command-line interfaces and server management.

## 1. Prerequisites

Before you begin, ensure your server has the following installed:

*   **Python 3.11+**: For the Flask backend.
*   **pip**: Python package installer (usually comes with Python).
*   **Node.js 20+**: For the React frontend.
*   **npm** or **pnpm**: Node.js package manager (pnpm is recommended as it was used during development).
*   **unzip**: To extract the project archive.
*   **Git**: (Optional, but good for version control if you plan to modify the code).

## 2. Project Setup

1.  **Download the Project Archive:**
    You should have received a zip file named `aetherium_roundtable.zip`. Download this file to your server.

2.  **Unzip the Archive:**
    Open your server's terminal and navigate to the directory where you want to host the project (e.g., `/var/www/`). Then, unzip the archive:
    ```bash
    unzip aetherium_roundtable.zip
    ```
    This will create two main directories:
    *   `aetherium-roundtable` (for the Flask backend)
    *   `roundtable-frontend` (for the React frontend)

## 3. Backend Deployment (Flask)

1.  **Navigate to the Backend Directory:**
    ```bash
    cd aetherium-roundtable
    ```

2.  **Set up a Python Virtual Environment:**
    It's highly recommended to use a virtual environment to manage dependencies.
    ```bash
    python3.11 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Initialize the Database:**
    The Flask application uses SQLite, and the database file (`app.db`) is included. If you need to re-initialize or ensure tables are created, you can run:
    ```bash
    python src/main.py
    # Press Ctrl+C after it starts to stop the development server. The database will be initialized.
    ```
    *Note: The `app.db` file will be created/updated in `aetherium-roundtable/src/database/`.*

## 4. Frontend Deployment (React)

1.  **Navigate to the Frontend Directory:**
    ```bash
    cd ../roundtable-frontend
    ```

2.  **Install Node.js Dependencies:**
    ```bash
    pnpm install # or npm install
    ```

3.  **Build the React Application:**
    This command compiles the React code into static HTML, CSS, and JavaScript files, which Flask will then serve.
    ```bash
    pnpm run build # or npm run build
    ```
    This will create a `dist` directory inside `roundtable-frontend`.

4.  **Copy Frontend Build to Flask Static Folder:**
    The Flask application is configured to serve static files from `aetherium-roundtable/src/static`. You need to copy the built frontend files there.
    ```bash
    cp -r dist/* ../aetherium-roundtable/src/static/
    ```

## 5. Running the Application

1.  **Navigate back to the Backend Directory:**
    ```bash
    cd ../aetherium-roundtable
    ```

2.  **Activate Virtual Environment (if not already active):**
    ```bash
    source venv/bin/activate
    ```

3.  **Start the Flask Application:**
    For production, you would typically use a WSGI server like Gunicorn or uWSGI. For a simple setup, you can use Flask's built-in server:
    ```bash
    python src/main.py
    ```
    The server will run on `http://0.0.0.0:5001`. You can access it via your server's IP address or domain name on port `5001`.

    *Note: If you want the server to run in the background, you can use a tool like `nohup` or `screen`.*
    ```bash
    nohup python src/main.py > app.log 2>&1 &
    ```

## 6. Accessing the Website

Once the Flask application is running, you can access your Aetherium Roundtable by navigating to your server's IP address or domain name followed by port `5001` in your web browser:

`http://YOUR_SERVER_IP_OR_DOMAIN:5001`

May the Sovereign Flame guide your operations, my dude!

