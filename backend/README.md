## To run backend separately
1. docker build -t <image_name> .
2. docker run -d --name <container_name> -p 8080:8080 --env-file .env <image_name> 