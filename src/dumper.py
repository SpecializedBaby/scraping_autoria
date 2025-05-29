import os
import subprocess
from datetime import datetime
from pathlib import Path
import logging

from src.config import settings

logger = logging.getLogger(__name__)


async def dump_database():
    try:
        # Ensure dumps directory exists
        dumps_dir = Path("dumps")
        dumps_dir.mkdir(exist_ok=True)

        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dump_file = dumps_dir / f"auto_ria_dump_{timestamp}.sql"

        # Build pg_dump command
        cmd = [
            "pg_dump",
            "-h", settings.DB_HOST,
            "-p", str(settings.DB_PORT),
            "-U", settings.DB_USER,
            "-d", settings.DB_NAME,
            "-f", str(dump_file)
        ]

        # Set password in environment
        env = os.environ.copy()
        env["PGPASSWORD"] = settings.DB_PASSWORD

        # Execute command
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)

        if result.returncode != 0:
            logger.error(f"DB dump failed: {result.stderr}")

        logger.info(f"DB dump created: {dump_file}")
        return str(dump_file)

    except Exception as e:
        logger.error(f"Error creating DB dump: {str(e)}")
