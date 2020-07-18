# Musify-dev-env
Servidor de aplicación API REST en Docker para Musify.

![Musify-dev-env CI](https://github.com/MauricioPortilla/Musify-dev-env/workflows/Musify-dev-env%20CI/badge.svg?branch=master)

## Contribuidores
- Cruz Portilla Mauricio
- Romero Peña Arturo Iván

## Requerimientos
- Docker
- Docker compose

## Instrucciones de ejecución
1. En una terminal, moverse al interior de la carpeta de este proyecto.
2. Ejecutar: `$ docker network create --driver bridge --subnet 172.250.6.0/24 musify_network` para crear la red entre los servidores.
3. Ejecutar: `$ docker-compose build`.
4. Ejecutar: `$ docker-compose up -d` para levantar el contenedor en segundo plano.

Una vez realizado esto, el servidor estará listo para su utilización.

### Servidores
- <a href="https://github.com/MauricioPortilla/Musify-db-env">Musify-db-env</a>: Servidor de Base de datos.
- <a href="https://github.com/MauricioPortilla/Musify-grpc-env">Musify-grpc-env</a>: Servidor de gRPC.

### Repositorios de servidores en DockerHub
- <a href="https://hub.docker.com/r/mauricioportilla/musify-dev-env">Musify-dev-env en DockerHub</a>
- <a href="https://hub.docker.com/r/mauricioportilla/musify-db-env">Musify-db-env en DockerHub</a>
- <a href="https://hub.docker.com/r/mauricioportilla/musify-grpc-env">Musify-grpc-env en DockerHub</a>

### Cliente
- <a href="https://github.com/MauricioPortilla/Musify">Musify</a>: Cliente de escritorio
- <a href="https://github.com/MauricioPortilla/MusifyMobile">MusifyMobile</a>: Cliente móvil
