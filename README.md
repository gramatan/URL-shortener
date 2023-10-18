# URL shortener.

Service for URL shortening.

Python, Poetry, Fastapi, Sqlalchemy, Postgresql, Docker, K8s.

## Launching the application in docker

```shell
docker build -t gran_url .
docker run -d -p 24501:24501 --name url_shortener gran_url
```

## Steps for deploying in kubernetes

From the [gran-url](gran-url) folder:
```shell
helm install gran-url ./gran-url/gran-url-0.1.0.tgz
```
