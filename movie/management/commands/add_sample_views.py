from django.core.management.base import BaseCommand
from movie.models import Movie
import random

class Command(BaseCommand):
    help = 'Agrega vistas de ejemplo a las películas existentes'

    def handle(self, *args, **options):
        movies = Movie.objects.all()
        
        for movie in movies:
            # Generar un número aleatorio de vistas entre 10 y 1000
            movie.views = random.randint(10, 1000)
            movie.save()
        
        self.stdout.write(
            self.style.SUCCESS(f'Se agregaron vistas de ejemplo a {movies.count()} películas')
        )