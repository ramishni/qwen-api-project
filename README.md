# Qwen3 FastAPI & Qwen-Agent Integration with Docker

This project integrates the Qwen3 large language model (running in LM Studio) with the Qwen-Agent framework, using a FastAPI backend as a proxy. The entire system is containerized with Docker for portability and ease of use, leveraging local GPU acceleration via LM Studio.

## Features

-   **FastAPI Proxy**: An asynchronous FastAPI server that forwards requests to LM Studio's OpenAI-compatible API.
-   **Streaming Support**: The proxy correctly handles streaming responses from the LLM, essential for conversational AI.
-   **Qwen-Agent Integration**: `agent_app.py` initializes a Qwen-Agent (`Assistant`) and connects it to the Qwen3 model through the local FastAPI proxy.
-   **Dockerized Environment**: `Dockerfile` and `start.sh` create a self-contained environment running both the FastAPI proxy and the Qwen-Agent.

## Prerequisites

1.  **Docker Desktop**: Ensure Docker Desktop is installed and running.
2.  **LM Studio**: Download, install, and run [LM Studio](https://lmstudio.ai/).
3.  **Qwen3 Model**: In LM Studio, download a Qwen3 model (e.g., `qwen2-7b-instruct-q4_k_m.gguf` or any other compatible GGUF model).

## Setup and Run

### 1. Configure LM Studio

1.  Open LM Studio.
2.  Go to the **Server** tab (the `<->` icon on the left).
3.  Select your downloaded Qwen3 model from the "Select a model to load" dropdown at the top.
4.  Under "Server Settings" (or similar section):
    -   Set **Server Host** to `0.0.0.0`. This is crucial for allowing Docker containers to access the LM Studio server.
    -   Note the **Port** (default is `1234`).
5.  Click **Start Server**.

### 2. Build and Run the Docker Container

1.  Open a terminal or PowerShell in the root directory of this project.
2.  Build the Docker image:
    ```bash
    docker build -t qwen-fastapi .
    ```
3.  Run the Docker container:
    ```bash
    docker run -p 8000:80 --name qwen-api --rm qwen-fastapi
    ```
    -   This command maps port `8000` on your host to port `80` inside the container.
    -   It runs the container in the foreground, so you'll see logs from both the FastAPI server and the Qwen-Agent.
    -   `--rm` ensures the container is removed when it stops.

### 3. Observe the System in Action

Once the container is running, you will see output in your terminal:

1.  The FastAPI server (Uvicorn) starting up.
2.  The `Qwen-Agent` application (`agent_app.py`) starting.
3.  Initialization messages from `Qwen-Agent` confirming it has connected to the LLM (via the proxy).
4.  The agent will then execute its pre-defined task (currently, it asks "Who are you and what can you do?").
5.  You will see the streaming response from the Qwen3 model, relayed through the FastAPI proxy and printed by the agent.

## How It Works

-   **LM Studio**: Runs on your host machine, serving the Qwen3 model via an OpenAI-compatible API (e.g., at `http://host.docker.internal:1234/v1/chat/completions` from the container's perspective).
-   **FastAPI Proxy (`main.py`)**: Runs inside the Docker container. It exposes an OpenAI-compatible endpoint at `/v1/chat/completions`. It receives requests from the `Qwen-Agent`, forwards them to LM Studio, and streams the responses back.
-   **Qwen-Agent (`agent_app.py`)**: Also runs inside the Docker container. It's configured to use the FastAPI proxy (`http://localhost:80/v1`) as its LLM service endpoint.
-   **Docker (`Dockerfile`, `start.sh`)**: The `Dockerfile` sets up the Python environment, installs all dependencies (FastAPI, Uvicorn, httpx, Qwen-Agent), and copies the application files. The `start.sh` script first launches the FastAPI server in the background, waits for it to be ready, and then executes `agent_app.py`.

## Customizing the Agent

To change the agent's behavior, initial prompt, or tasks:

1.  Modify the `agent_app.py` script.
    -   For example, change the `messages` list in the `run_agent_task` function to ask different questions or provide different system prompts.
2.  Rebuild the Docker image:
    ```bash
    docker build -t qwen-fastapi .
    ```
3.  Run the container again:
    ```bash
    docker run -p 8000:80 --name qwen-api --rm qwen-fastapi
    ```

## API Documentation (Proxy)

If you wish to interact with the FastAPI proxy directly (e.g., for testing or from another application), its OpenAPI documentation is available at [http://localhost:8000/docs](http://localhost:8000/docs) while the container is running.
