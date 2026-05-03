docker compose -p app-dev --env-file .env.dev -f compose.yaml -f compose.dev.yaml pull
docker compose -p app-dev --env-file .env.dev -f compose.yaml -f compose.dev.yaml up -d
docker compose -p app-dev ps