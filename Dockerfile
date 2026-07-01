# Dockerfile for AcePilot AI (Cloud Run deployment)
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose Streamlit port
EXPOSE 8080

# Run Streamlit (Cloud Run uses PORT env variable)
CMD streamlit run frontend/streamlit_app.py \
    --server.port=${PORT:-8080} \
    --server.address=0.0.0.0 \
    --server.headless=true
