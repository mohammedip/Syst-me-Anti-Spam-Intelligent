FROM python:3.11-slim

# -----------------------------------------------------
# Install system deps (Java for PySpark + build tools)
# -----------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-jre \
    default-jdk \
    build-essential \
    libpng-dev \
    libjpeg-dev \
    libfreetype6-dev \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH="${JAVA_HOME}/bin:${PATH}"
ENV PYTHONUNBUFFERED=1

# -----------------------------------------------------
# Create working directory
# -----------------------------------------------------
WORKDIR /app

# -----------------------------------------------------
# Install Python dependencies first (cached)
# -----------------------------------------------------
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt && \
    pip install --no-cache-dir jupyter

# -----------------------------------------------------
# Copy project files
# -----------------------------------------------------
COPY . /app

# -----------------------------------------------------
# Expose ports:
# 8501 → Streamlit UI
# 8888 → Jupyter Notebook
# -----------------------------------------------------
EXPOSE 8501
EXPOSE 8888

# -----------------------------------------------------
# CMD runs both Streamlit AND Jupyter at container startup
# -----------------------------------------------------
CMD bash -c "\
    jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root --ServerApp.token='' \
        --ServerApp.password='' \
        --ServerApp.disable_check_xsrf=True & \
    streamlit run app/streamlit_app.py --server.port=8501 --server.address=0.0.0.0 --server.enableCORS=false \
"
