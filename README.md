# AutoRia Car Scraper

A Python application for scraping used car listings from AutoRia.com with PostgreSQL storage, scheduled tasks, and database backups.

## Features

- Daily scraping of AutoRia used car listings
- Data storage in PostgreSQL
- Automatic daily database dumps
- Docker-compose deployment
- Async scraping with httpx + selectolax
- Alembic database migrations
- Scheduled tasks with APScheduler

## Prerequisites

- Docker
- Python 3.11+
- PostgreSQL client tools (for dumps)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/auto-ria-scraper.git
cd auto-ria-scraper
```

2. Create and configure `.env` file:
```bash
cp .env.example .env
```

3. Build and start containers:
```bash
docker-compose up -d --build
```

## Usage

### Normal Operation
```bash
docker-compose up -d
```

### Manual Scraping (for debugging)
```bash
docker-compose run --rm scraper python src/main.py
```

### Database Access
```bash
docker-compose exec db psql -U postgres -d auto_ria
```

### View Logs
```bash
docker-compose logs -f scraper
```

## Project Structure

```
scraping_autoria/
├── alembic/               # Database migrations
├── dumps/                 # Database dump files
├── src/
│   ├── database/          # DB models and session
│   ├── scraper/           # Scraping components
│   ├── dumper.py          # DB backup utility
│   ├── scheduler.py       # Task scheduling
│   └── main.py            # Main application
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## License

MIT License


