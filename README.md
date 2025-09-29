# API Flask con Neo4j

API simple construida con Flask y Neo4j para gestionar personas en una base de datos de grafos.

## Requisitos

- Docker
- Docker Compose

## Cómo usar

1. Iniciar los servicios:
   ```bash
   docker-compose up -d
   ```

2. La API estará disponible en: http://localhost:5001

3. Neo4j Browser estará disponible en: http://localhost:7474
   - Usuario: neo4j
   - Contraseña: supersecurepassword

## Endpoints

- `GET /` - Documentación de la API
- `GET /persons` - Obtener todas las personas
- `POST /persons` - Crear una nueva persona
- `GET /health` - Verificar estado de la API y conexión a Neo4j

## Imágenes

![1](https://raw.githubusercontent.com/sebas1541/taller-15-setp-dist/main/images/1.png)

![2](https://raw.githubusercontent.com/sebas1541/taller-15-setp-dist/main/images/2.png)

![3](https://raw.githubusercontent.com/sebas1541/taller-15-setp-dist/main/images/3.png)

![4](https://raw.githubusercontent.com/sebas1541/taller-15-setp-dist/main/images/4.png)

## Estructura del Proyecto

```
.
├── app.py           # Aplicación Flask
├── docker-compose.yml  # Configuración de Docker
├── Dockerfile       # Configuración de la imagen de la API
└── requirements.txt # Dependencias de Python
```

## Comandos útiles

- Ver logs de los contenedores:
  ```bash
  docker-compose logs -f
  ```

- Detener los servicios:
  ```bash
  docker-compose down
  ```

- Eliminar volúmenes (incluyendo datos de Neo4j):
  ```bash
  docker-compose down -v
  ```

## Variables de Entorno

Si necesitas ejecutar la aplicación fuera de Docker:

```bash
export NEO4J_URI=bolt://localhost:7687
export NEO4J_USER=neo4j
export NEO4J_PASSWORD=supersecurepassword
```

| Variable | Valor por defecto | Descripción |
|----------|------------------|-------------|
| `NEO4J_URI` | `bolt://localhost:7687` | URL de conexión a Neo4j |
| `NEO4J_USER` | `neo4j` | Usuario de Neo4j |
| `NEO4J_PASSWORD` | `supersecurepassword` | Contraseña de Neo4j |
| `FLASK_ENV` | `production` | Entorno de Flask (production/development) |
| `FLASK_PORT` | `5000` | Puerto de la aplicación Flask |
docker-compose up -d

# View logs
docker-compose logs -f flask_api

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## Data Structure

The API serves data from a Neo4j database containing:
- **10,000 users** with properties: id, name, email, department, salary, age, city, joinDate
- **35,000+ friendships** between users
- **266 management relationships** (MANAGES relationships)

## Pagination

- **Default limit:** 50 entries per page
- **Maximum limit:** 100 entries per page
- **Navigation:** Use `hasNext` and `hasPrev` in response to determine pagination
- **Total pages:** Available in `pagination.pages`
