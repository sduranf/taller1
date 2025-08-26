from django.core.management.base import BaseCommand
from movie.models import Movie
import os
import json

class Command(BaseCommand):
    help = 'Load movies from IMDbMovies.json into the Movie model'

    def handle(self, *args, **kwargs):
        # Construct the full path to the JSON file
        #Recuerde que la consola está ubicada en la carpeta DjangoProjectBase.
        #El path del archivo IMDbMovies con respecto a DjangoProjectBase sería la carpeta anterior
        json_file_path = 'movie/management/commands/IMDbMovies.json' 
        
        # Load data from the JSON file
        with open(json_file_path, 'r') as file:
            movies = json.load(file)
        
        # Add movies to the database
        cont = 0
        for i in range(100):
            movie = movies[i]
            exist = Movie.objects.filter(title = movie['Title']).first() #Se asegura que la película no exista en la base de datos
            if not exist:
                try:              
                    Movie.objects.create(title = movie['Title'],
                                        image = 'movie/images/default.JPG',
                                        genre = movie['Main Genres'],
                                        year = movie['Release Year'],
                                        description = movie['Summary'],)
                    cont += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error creating movie {movie["Title"]}: {str(e)}'))
                    pass        
            else:
                try:
                    exist.title = movie["Title"]
                    exist.image = 'movie/images/default.JPG'
                    exist.genre = movie["Main Genres"]
                    exist.year = movie["Release Year"]
                    exist.description = movie["Summary"]
                    exist.save()
                    cont += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error updating movie {movie["Title"]}: {str(e)}'))
                    pass
        
        self.stdout.write(self.style.SUCCESS(f'Successfully processed {cont} movies in the database'))