local-start-app:
	docker-compose --env-file .env.local -f docker-compose.local.yaml up -d --build

local-down-app:
	docker-compose --env-file .env.local -f docker-compose.local.yaml down

init-alembic:
	alembic init migrations

create-migration:
	alembic revision -m "${name}"

local-migration-up:
	alembic -x env_path=".env.local" upgrade head