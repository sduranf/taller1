"""from django.shortcuts import render
from .models import Movie

def statistics(request):
    movies = Movie.objects.all()
    genre_count = {}

    for movie in movies:
        # Suponiendo que movie.genres es un ManyToManyField o lista de strings
        first_genre = None
        if hasattr(movie, 'genres'):
            # Si es ManyToManyField
            if hasattr(movie.genres, 'all'):
                genres = list(movie.genres.all())
                if genres:
                    first_genre = str(genres[0])
            # Si es lista de strings
            elif isinstance(movie.genres, list) and movie.genres:
                first_genre = movie.genres[0]
        if first_genre:
            genre_count[first_genre] = genre_count.get(first_genre, 0) + 1

    genre_labels = list(genre_count.keys())
    genre_counts = list(genre_count.values())

    return render(request, 'statistics.html', {
        'genre_labels': genre_labels,
        'genre_counts': genre_counts,
    })"""