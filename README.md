# Books API Backend

Este es un proyecto de backend desarrollado en Django REST Framework (DRF) que utiliza MongoDB como base de datos para gestionar información de libros. La aplicación proporciona una API REST para realizar operaciones CRUD y una funcionalidad adicional para obtener el precio promedio de los libros publicados en un año específico.

## Requerimientos

- Python 3.8+
- Django
- Django REST Framework
- MongoDB
- Pymongo
- Docker (OPCIONAL)
- Docker Compose (OPCIONAL)

## Configuración del Proyecto

### Clona el repositorio

```bash
https://github.com/tu_usuario/books-api.git
cd books-api
```
## CONFIGURACIÓN CON DOCKER

### 1. Ejecuta Docker Compose para construir y arrancar el contenedor
```bash
docker compose up --build -d
```
 
### 2. Verifica que este corriendo los contenedores

```bash
docker ps
```

### 3. Ejecuta el script de seed para añadir datos iniciales:

```bash
docker exec web python run_seed_data.py
```


## CONFIGURACIÓN CON PYTHON

### * Debe tener instalado Python 3.11 y mongoDB

### 1. Crea un entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instala las dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecuta el script de seed para añadir datos iniciales:

```bash
python run_seed_data.py
```

### 4. Crea las migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Inicia el servidor

```bash
python manage.py runserver
```

## UNIT TEST

### Ejecuta el script de unit test

```bash
# Usando docker
docker exec web python manage.py test

# Usando python
python manage.py test
```

## Visualización Swagger de los Endpoints

Para visualizar la API en Swagger, visita `http://localhost:8000/`.


### CRUD de Libros

- **GET** `/api/books/` - Lista todos los libros
- **GET** `/api/books/?<param>=<value>` - Obtiene un libro por query_params, son: title, author, published_date, genre, price
- **POST** `/api/books/` - Crea un nuevo libro
- **PUT** `/api/books/` - Actualiza un libro existente
- **DELETE** `/api/books/` - Elimina un libro por su ID

### Agregación: Precio Promedio por Año

- **GET** `/api/books/average-price/?year=<year>` - Obtiene el precio promedio de los libros publicados en el año especificado


## Importa la colección de postman

El archivo `SEEK _BOOK_APP.postman_collection.json` contiene los datos de ejemplo para la colección de usuarios y books. Puedes importarlo en Postman o usar la API de usuarios de tu aplicación Django.


## API de Usuarios

###  Crea un usuario en la API usando curl o Postman

La API estará disponible en `http://localhost:8000/api/users/register/`.

```bash
curl --location --request POST 'http://localhost:8000/api/users/register/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "testuser",
    "password": "testpassword",
    "nombres": "John",
    "apellidos": "Doe",
    "email": "0aOY5@example.com"
}'
``` 

### Agrega el token al header de la solicitud para usar la API de CRUD de libros

```bash
curl --location --request GET 'http://localhost:8000/api/books/' \
--header 'Authorization: Token <tu-token>'

En Postman, puedes agregar el token en la sección de encabezados de la solicitud.
Authorization: Token <tu-token>
```



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
