# ---- Build Stage ----
# Use a full Python image to ensure build tools are available for dependencies
FROM python:3.11 as builder

# Set the working directory
WORKDIR /app

# Install dependencies
# First, copy only requirements.txt to leverage Docker layer caching
COPY requirements.txt .

# Create a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies into the virtual environment
RUN pip install --no-cache-dir -r requirements.txt

# ---- Final Stage ----
# Use a lightweight slim image for the final container
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy the application code
COPY . .

# Make the startup script executable
RUN chmod +x start.sh

# Set the PATH to use the virtual environment's Python and packages
ENV PATH="/opt/venv/bin:$PATH"

# Set the startup command
CMD ["./start.sh"]