First commit# Books API Backend

Este es un proyecto de backend desarrollado en Django REST Framework (DRF) que utiliza MongoDB como base de datos para gestionar información de libros. La aplicación proporciona una API REST para realizar operaciones CRUD y una funcionalidad adicional para obtener el precio promedio de los libros publicados en un año específico.

## Requerimientos
- Python 3.8+
- Django
- Django REST Framework
- MongoDB
- Pymongo

## Configuración del Proyecto

### 1. Clona el repositorio
```bash
https://github.com/tu_usuario/books-api.git
cd books-api
```

### 2. Crea un entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instala las dependencias
```bash
pip install -r requirements.txt
```

### 4. Configura la conexión con MongoDB
Edita el archivo `settings.py` y añade la configuración de tu instancia de MongoDB:
```python
# MongoDB Config
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "books_db"
```

### 5. Inicializa la base de datos con datos de prueba
Ejecuta el script de seed para añadir datos iniciales:
```bash
python books/migrations/seed_data.py
```

### 6. Ejecuta el servidor de desarrollo
```bash
python manage.py runserver
```

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

## Contribuciones
Si deseas contribuir a este proyecto, por favor realiza un fork del repositorio, crea una rama con tus cambios y envía un pull request.

## Licencia
Este proyecto está bajo la Licencia MIT. Puedes ver el archivo [LICENSE](LICENSE) para más detalles.

