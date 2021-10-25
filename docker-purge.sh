# shut down all containers (remove images and volumes)
docker-compose -f docker-compose-production.yml down --volumes --rmi local

# make sure containers are removed (if not running)
docker container rm -f fbc_curation_nginx_1
docker container rm -f fbc_curation_backend_1
docker container rm -f fbc_curation_frontend_1
docker container rm -f frog_nginx_1
docker container rm -f frog_backend_1
docker container rm -f frog_frontend_1
docker container rm -f frog_redis_1
docker container rm -f frog_worker_1
docker container rm -f frog_dashboard_1


# make sure images are removed
docker image rm -f fbc_curation_nginx:latest
docker image rm -f fbc_curation_backend:latest
docker image rm -f fbc_curation_frontend:latest
docker image rm -f frog_nginx:latest
docker image rm -f frog_backend:latest
docker image rm -f frog_frontend:latest
docker image rm -f frog_redis:latest
docker image rm -f frog_worker:latest
docker image rm -f frog_dashboard:latest

# make sure volumes are removed
docker volume rm -f fbc_curation_node_modules
docker volume rm -f fbc_curation_vue_dist

# cleanup all dangling images, containers, volumes and networks
docker system prune --force
