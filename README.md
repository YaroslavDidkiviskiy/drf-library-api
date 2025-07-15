# 📚 DRF Library API - Docker Edition

A complete Dockerized solution for book library management using Django REST Framework.

## 🐳 Docker Installation

### Prerequisites
- Docker installed ([Download Docker](https://www.docker.com/get-started))
- Docker Compose (included with Docker Desktop)

### Step-by-Step Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YaroslavDidkivskiy/drf-library-api.git
   cd drf-library-api
Create environment file:

   ```bash
   cp .envsample .env
Edit the .env file with your configuration.

Build and launch containers:

   ```bash
   docker-compose up --build -d
Apply database migrations:

   ```bash
   docker-compose exec app python manage.py migrate
Create superuser (optional):

   ```bash
docker-compose exec app python manage.py createsuperuser
