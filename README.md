# romantig_ROSEAP

navigate to oee-service folder and build the image for the OEE microservice:

```
  cd oee-service

  docker build -t rose-ap-oee .
```
Now go back to the main folder, make the `./services` script executable
```
  cd ..
  sudo chmod +x ./services
```
Run  `sudo ./services create` to create all images, then run `./services start` to start all containers.
```

Now you can open Grafana on localhost:3000 and select "Process Status" dashboard to visualiza OEE live data
