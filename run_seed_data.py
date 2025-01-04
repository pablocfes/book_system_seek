import os
from django.core.management import execute_from_command_line

# Establece el módulo de configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seek.settings')

import django
django.setup()

# Llama a la función seed_data
from books import seed_data


if __name__ == "__main__":
    seed_data.insert_initial_data()
