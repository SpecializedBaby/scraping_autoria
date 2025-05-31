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

        # Set password in environment
        env = os.environ.copy()
        env["PGPASSWORD"] = settings.DB_PASSWORD

        cmd = [
            "docker", "exec", "-i", settings.POSTGRES_CONTAINER,
            "pg_dump",
            "-U", settings.DB_USER,
            settings.DB_NAME
        ]

        # Execute command
        with open(dump_file, "w") as f:
            result = subprocess.run(cmd, env=env, stdout=f, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            logger.error(f"DB dump failed: {result.stderr}")

        logger.info(f"DB dump created: {dump_file}")
        return str(dump_file)

    except Exception as e:
        logger.error(f"Error creating DB dump: {str(e)}")
