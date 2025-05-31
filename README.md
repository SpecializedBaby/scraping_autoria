# 🚗 Auto RIA Scraper

A fast and efficient asynchronous scraper for auto.ria.com, built with httpx, selectolax, and asyncio. Scraped data is stored in a PostgreSQL database running in Docker. Includes database dump functionality.

## 📦 Features

- 🔍 Async scraping with robust error handlings
- 🧠 Fast HTML parsing using ```selectolax```
- 🐘 PostgreSQL integration via Docker
- 💾 Database dump to local ```.sql``` file
- 📄 Configurable via environment variables
- 🧪 Easy to extend for new data types or pages

## ⚙️ Requirements

- Python 3.10+
- Docker + Docker Compose
- PostgreSQL client (```pg_dump``` inside container)

## 🐳 Setup with Docker

1. Create a .env file from .env.example
2. Run container:
```bash
docker-compose up --build
```

## Project Structure

```
src/
  scraper/          # Scraper logic
  database/         # SQLAlchemy models
  logs/
  main.py
  dumper.py   
  scheduler.py      # Scheduled scraping task
  config.py         # Settings from env
  utils/dump.py     # DB dump script
dumps/              # Saved .sql dumps
alembic/            # DB migrations
....
```

## 🧑‍💻 Author

Dmytro
https://github.com/SpecializedBaby

## License

MIT License


