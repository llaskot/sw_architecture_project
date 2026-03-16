
# 🚀 FastAPI Learning Project

A clean and modern starter project using **FastAPI**, **Pydantic**, and **uv** for package management.

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
powershell -c "ir | iex" (irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1))
```
**macOS / Linux::**
```Bash
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
```

1. **Clone the repository:**
   ```bash
   git clone git@github.com:llaskot/sw_architecture_project.git
   cd pashnev_project
   
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

# 4. Build and run Mongo DB in container
```commandline
docker-compose up -build
```

# 5. Run the server
fastapi dev main.py