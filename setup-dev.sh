if [ ! -f .env ]; then
    cp .env-example .env
fi

docker compose up -d

docker compose run backend alembic upgrade head