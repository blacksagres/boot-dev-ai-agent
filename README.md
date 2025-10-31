# boot-dev-ai-agent

This project is a minimal Python application managed with `uv`.

## Setup Instructions

To get this project up and running, follow these steps:

### 0. Set up Virtual Environment

It is highly recommended to set up a virtual environment (`.venv`) to manage project dependencies. You can create and activate it using `uv`:

```bash
uv venv
source .venv/bin/activate
```

### 1. Install `uv`

If you don't have `uv` installed, you can install it using `pipx` (recommended) or `pip`:

```bash
pip install pipx
pipx ensurepath
pipx install "uv==0.1.18"
```

Alternatively, with `pip`:

```bash
pip install "uv==0.1.18"
```

### 2. Install Dependencies

Navigate to the project directory and install the required dependencies:

```bash
uv sync
```

### 3. Run the Application

Execute the `main.py` file to run the application:

```bash
python main.py
```

This will print "Hello from boot-dev-ai-agent!" to your console.
