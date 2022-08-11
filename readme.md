navigate to oee-service folder

docker build -t rose-ap-oee .

cd ..

sudo chmod +x ./services
sudo ./services create

./services start

open Grafana on localhost:3000 and select "Process Status" dashboard to visualiza OEE live data