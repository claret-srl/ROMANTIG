# Docker
## Copy from container to host
docker cp grafana:/etc/grafana/provisioning/dashboards/dashboard.yaml C:/Users/User/Documents/GitHub/Claret/romantig_RAMP_ROSEAP/dev/grafana/copyFromContainer/dashboard.yaml

docker rm $(docker ps -a | grep -v "my_docker" | awk 'NR>1 {print $1}')
docker rm $(docker ps -a | grep -v "my_docker")
docker rm $(docker ps -a | grep --invert "my_docker")
docker volume rm $(docker ps -a | grep --invert "my_docker")
docker image rm $(docker ps -a | grep --invert "my_docker")

docker image rm $(docker image ls -a | grep  "<none>")
docker volume rm $(docker volume ls | grep --invert "fiware")
docker volume rm $(docker volume ls -q | grep --invert "fiware")

docker volume rm $(docker volume ls | grep "mongo")

docker volume prune