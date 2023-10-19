# URL shortener.

Service for URL shortening.

Python, Poetry, Fastapi, Sqlalchemy, Postgresql, Docker, K8s.

## Launching the application in docker

```shell
docker build -t gran_url .
docker run -d -p 24501:24501 --name url_shortener gran_url
```

## Steps for deploying in kubernetes

Create package and install:
```shell
helm package gran-url/.
helm install gran-url gran-url-0.1.1.tgz
```

For port-forward(after start) do:
```shell
kubectl port-forward svc/gran-url 24501:24501
```
