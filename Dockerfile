FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml backend/requirements.txt ./
RUN pip install --no-cache-dir -e .
COPY . .
ENV AUDIOHARDCORE_ENV=production
ENV AUDIOHARDCORE_DATA_DIR=/data
EXPOSE 8765
CMD ["uvicorn","backend.app.main:app","--host","0.0.0.0","--port","8765"]
