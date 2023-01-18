# CONTRIBUTING

## How to run the Dockerfile locally

## Build Docker Image (image named warehouse-database-api)...
```
docker build -t warehouse-database-api .
```
## Build the Docker container to run with volume (container named project-09-digiwares)...
```
docker run --name digiwares-flask-api -dp 5000:5000 -w /app -v "/c/Users/caaus/OneDrive/Desktop/P/Projects/Project 09 Digiwares/CODE:/app"  warehouse-database-api
```
```
How this is supposedly done on a Mac, I have not verified this...
Mac:
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" IMAGE_NAME sh -c "flask run"

```
