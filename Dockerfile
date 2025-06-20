FROM apache/airflow:2.8.3-python3.8

USER root

# ติดตั้ง dependencies ด้วย apt-get แทนการใช้ playwright install-deps
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    unzip \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxcb1 \
    libxkbcommon0 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    libatspi2.0-0 \
    fonts-noto-color-emoji \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
    
RUN apt-get update && apt-get install -y xvfb

USER airflow

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ติดตั้ง Playwright โดยไม่ต้องรัน install-deps แยก
RUN playwright install chromium

ENV PYTHONPATH "${PYTHONPATH}:/opt/airflow/dags"

COPY dags/ /opt/airflow/dags/
COPY dags/scripts/ /opt/airflow/scripts/
COPY credentials/ /opt/airflow/credentials/