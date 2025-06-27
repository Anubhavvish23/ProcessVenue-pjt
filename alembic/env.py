from logging.config import fileConfig
import os
from sqlalchemy import pool
from alembic import context

# ✅ Load .env if needed
from dotenv import load_dotenv
load_dotenv()

# ✅ Import your SQLAlchemy Base and engine from FastAPI
from app.models import Base
from app.database import engine

# Alembic Config
config = context.config

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ✅ Set target metadata (used for autogenerate)
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode using our FastAPI engine."""
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
