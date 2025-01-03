# Books API Backend

Este es un proyecto de backend desarrollado en Django REST Framework (DRF) que utiliza MongoDB como base de datos para gestionar información de libros. La aplicación proporciona una API REST para realizar operaciones CRUD y una funcionalidad adicional para obtener el precio promedio de los libros publicados en un año específico.

## Requerimientos
- Python 3.8+
- Django
- Django REST Framework
- MongoDB
- Pymongo
- Docker
- Docker Compose

## Configuración del Proyecto

### 1. Clona el repositorio
```bash
https://github.com/tu_usuario/books-api.git
cd books-api
```

### 2. Configura Docker y Docker Compose
#### Crea un archivo `Dockerfile` para la aplicación Django:
```Dockerfile
# Dockerfile
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de la aplicación
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto de Django
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

#### Crea un archivo `docker-compose.yml` para orquestar los servicios de Django y MongoDB:
```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - MONGO_URI=mongodb://db:27017/
      - MONGO_DB=books_db
    depends_on:
      - db

  db:
    image: mongo:5.0
    container_name: mongo
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

volumes:
  mongo_data:
```

### 3. Inicializa la base de datos con datos de prueba
Ejecuta el script de seed para añadir datos iniciales:
```bash
docker-compose run web python books/migrations/seed_data.py
```

### 4. Levanta los servicios
```bash
docker-compose up
```

### 5. Accede a la aplicación
La API estará disponible en `http://localhost:8000/api/`.

## Endpoints Disponibles

### CRUD de Libros
- **GET** `/api/books/` - Lista todos los libros
- **POST** `/api/books/` - Crea un nuevo libro
- **GET** `/api/books/<id>/` - Obtiene un libro por su ID
- **PUT** `/api/books/<id>/` - Actualiza un libro existente
- **DELETE** `/api/books/<id>/` - Elimina un libro por su ID

### Agregación: Precio Promedio por Año
- **GET** `/api/books/average-price/<year>/` - Obtiene el precio promedio de los libros publicados en el año especificado

## Ejemplo de Datos de Prueba
```json
[
  {
    "title": "Book One",
    "author": "Author A",
    "published_date": "2021-06-01",
    "genre": "Fiction",
    "price": 15.99
  },
  {
    "title": "Book Two",
    "author": "Author B",
    "published_date": "2020-07-15",
    "genre": "Non-Fiction",
    "price": 20.00
  }
]
```

## Herramientas Utilizadas
- Django
- Django REST Framework
- MongoDB
- Pymongo
- Docker
- Docker Compose

## Contribuciones
Si deseas contribuir a este proyecto, por favor realiza un fork del repositorio, crea una rama con tus cambios y envía un pull request.

## Licencia
Este proyecto está bajo la Licencia MIT. Puedes ver el archivo [LICENSE](LICENSE) para más detalles.

