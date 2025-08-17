FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose ports
EXPOSE 8000 8001 8002

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Command to run when the container starts
CMD ["python", "mcp_server.py"] 