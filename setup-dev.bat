if not exist .env (
    copy .env.example .env
)

docker compose up -d

docker compose run backend sh setup/setup_db.sh
