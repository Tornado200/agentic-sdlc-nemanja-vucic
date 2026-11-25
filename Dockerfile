FROM python:3.12-slim

WORKDIR /app

# Copy project definition and package first so the install layer is cached
COPY pyproject.toml .
COPY mars_rover/ mars_rover/
RUN pip install --no-cache-dir -e ".[dev]"

# Copy tests last (changes most often)
COPY tests/ tests/

# Run tests by default
CMD ["pytest", "tests/", "-v", "--tb=short"]
