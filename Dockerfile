# Stage 1: Builder Stage - Install dependencies
# Use the official Python slim image matching the project's version
FROM python:3.10-slim as builder

# Set working directory
WORKDIR /app

# Install uv - the fast Python package installer
# We install it here to leverage its speed for dependency installation
RUN pip install uv

# Copy only the dependency definition file first to leverage Docker cache
COPY pyproject.toml ./

# Install dependencies using uv
# This installs dependencies into the system site-packages within this stage
# We don't need dev dependencies for the final image
RUN uv pip install --system --no-deps .

# Stage 2: Final Stage - Setup the runtime environment
# Use the same slim base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Create a non-root user and group
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --ingroup appgroup --no-create-home appuser

# Copy installed dependencies from the builder stage's site-packages
# Adjust the path according to the Python version's site-packages location
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# Copy the application source code
COPY ./src ./src

# Copy configuration directory if needed (adjust if config files are used)
# COPY ./config ./config

# Change ownership of the application directory to the non-root user
# Ensure the user can write logs or cache files if needed (adjust permissions accordingly)
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Expose the port the application runs on (should match config/defaults)
EXPOSE 8000

# Command to run the application using uvicorn
# Use the host and port configured for the application
# Note: We run uvicorn directly as it was installed as a dependency
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
