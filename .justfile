set dotenv-load := true

compose := "docker compose --env-file .dev.env"

app:
    {{compose}} -f docker_compose/app.yaml up -d --build

app-down:
    {{compose}} -f docker_compose/app.yaml down

pg:
    {{compose}} -f docker_compose/pg.yaml up -d

pg-down:
    {{compose}} -f docker_compose/pg.yaml down

minio:
    {{compose}} -f docker_compose/minio.yaml up -d

minio-down:
    {{compose}} -f docker_compose/minio.yaml down

redis:
    {{compose}} -f docker_compose/redis.yaml up -d

redis-down:
    {{compose}} -f docker_compose/redis.yaml down

alembic-upgrade-head:
    uv run alembic upgrade head
