# Syst-me-Anti-Spam-Intelligent

This project provides a spam detection/analysis pipeline using PySpark. The repository now includes a Dockerfile and docker-compose configuration to run a minimal Streamlit app that demonstrates the preprocessing pipeline.

## Run with Docker

Ensure you have Docker and docker-compose installed. From the project root, run:

```powershell
docker-compose up --build
```

Open your browser to http://localhost:8501 to see the Streamlit app. The Streamlit app uses PySpark in local mode and runs a small sample form the dataset.

If you prefer to run without docker, create a virtualenv and install the dependencies:

```powershell
python -m venv venv; .\venv\Scripts\Activate
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

Note: The Docker image includes OpenJDK to satisfy Spark runtime requirements and installs system libs needed by the WordCloud and Pillow packages.

## Run Jupyter (Lab) in Docker

You can run a Jupyter Lab instance that uses the same image and dataset. Build and start only the notebook service:

```powershell
docker compose up --build notebook
```

Open http://localhost:8888 in your browser and enter the token printed by the container logs.
To print logs and find the token (or if you used the `JUPYTER_TOKEN` env var, use that token):

```powershell
docker compose logs -f notebook
```

If you'd prefer to use a static token in `docker-compose.yml`, it's already configured as `JUPYTER_TOKEN=devtoken` for convenience (dev only). For production use, do not expose a tokenless or static token.

