# 🚀 FastAPI Learning Project

A clean and modern starter project using **FastAPI**, **Pydantic**, and **uv** for package management.

---

## 🐳 Full Application Deployment (Staged / Docker Compose)

This project includes a complete Docker Compose setup in the `staged/` directory. It automatically spins up the MongoDB database, the FastAPI backend, and a React frontend (served via Nginx). The frontend is built dynamically by pulling the latest code from its repository.

### 1. Configure Environment
First, create your environment variables file using the provided example:
```bash
cp staged/.env.example staged/.env
```
*(Open `staged/.env` and review the variables. Ensure `VITE_API_URL=/api` is set correctly for Nginx routing).*

### 2. Build and Run
Navigate to the `staged/` directory and start the services. 
*Note: The `docker-compose.yaml` is configured to always pull the latest frontend code and build it without using the cache.*
```bash
cd staged
docker compose up -d
```

### 3. Access the Services
Once all containers are healthy and running, you can access the project here:
* 🖥️ **Frontend (UI):** http://localhost:8050
* 📖 **Backend API Docs (Swagger):** http://localhost:8080/docs
* 🗄️ **MongoDB:** localhost:27018

### 4. Stopping the Application
To stop the application and clean up the containers:
```bash
docker compose down
```
*(Add the `-v` flag if you want to completely wipe the database volume).*

---


###   DEv MODE

## 🛠 Prerequisites

Before you begin, ensure you have the following installed:
* **Python 3.13+**
* **Docker**
* **uv** (Recommended) — A lightning-fast Python package manager.

## ⚡ Quick Start (with `uv`)

This project uses `uv` to manage dependencies and virtual environments. It's much faster than standard `pip`.



A clean and modern starter project using **FastAPI**, **Pydantic**, and **uv** for package management.

---

## 🛠 Prerequisites

Before you begin, ensure you have **Python 3.13+** installed on your system.

### Install `uv` (The Package Manager)
`uv` is a lightning-fast Python package manager. It is highly recommended to use it for this project.

**Windows (PowerShell):**
```powershell
powershell -c "ir | iex" (irm https://astral.sh/uv/install.ps1)
```
**macOS / Linux::**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

1. **Clone the repository:**
   ```bash
   git clone git@github.com:llaskot/sw_architecture_project.git
   cd pashnev_project
   ```
   
# 1.1. Build and run Mongo DB in container
```commandline
docker-compose up --build
```
   
# 1.2. Create .env using .env.example as an example


# 2. Sync dependencies using uv
# This creates .venv and installs everything from uv.lock in one go
```commandline
uv sync
```

# 3. Run the development server
# The 'dev' mode enables auto-reload on code changes
```commandline
uv run fastapi dev main.py
```
# --- OR (Alternative without uv) ---

# 2. Create and activate virtual environment
```commandline
python -m venv .venv
```

# On Windows:
```commandline
.venv\Scripts\activate
```

# On macOS/Linux:
# source 
```commandline
.venv/bin/activate
```

# 3. Install dependencies manually
### Installation
Install all dependencies directly from `pyproject.toml`:
```bash
pip install
```

# 5. Run the server
```commandline
fastapi dev main.py
```