import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64


from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
from django.db import models

def home(request):

    
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies })

    
def about(request):
    return render(request, 'about.html')

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})


def statistics_view(request):
    matplotlib.use('Agg')
    
    # Primera gráfica: Películas por año
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')
    movie_counts_by_year = {}
    
    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = "None"
        count = movies_in_year.count()
        movie_counts_by_year[year] = count

    # Crear la primera gráfica
    plt.figure(figsize=(10, 6))
    bar_width = 0.5
    bar_spacing = 0.5
    bar_positions = range(len(movie_counts_by_year))
    
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center', color='skyblue')

    plt.title('Número de Películas por Año')
    plt.xlabel('Año')
    plt.ylabel('Número de Películas')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    buffer1 = io.BytesIO()
    plt.savefig(buffer1, format='png')
    buffer1.seek(0)
    plt.close()

    image_png1 = buffer1.getvalue()
    buffer1.close()
    graphic1 = base64.b64encode(image_png1)
    graphic1 = graphic1.decode('utf-8')

    # Segunda gráfica: Vistas por género
    # Obtener todas las películas y procesar solo el primer género de cada una
    movies = Movie.objects.all()
    views_by_genre = {}
    
    for movie in movies:
        if movie.genre and movie.genre.strip():
            # Dividir por comas y tomar solo el primer género
            first_genre = movie.genre.split(',')[0].strip()
            if first_genre:
                if first_genre in views_by_genre:
                    views_by_genre[first_genre] += movie.views
                else:
                    views_by_genre[first_genre] = movie.views

    # Crear la segunda gráfica
    plt.figure(figsize=(12, 6))
    if views_by_genre:
        bar_positions2 = range(len(views_by_genre))
        plt.bar(bar_positions2, views_by_genre.values(), width=0.6, align='center', color='lightcoral')
        
        plt.title('Cantidad de Vistas por Género')
        plt.xlabel('Género')
        plt.ylabel('Total de Vistas')
        plt.xticks(bar_positions2, views_by_genre.keys(), rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.2)
    else:
        plt.text(0.5, 0.5, 'No hay datos de vistas por género', ha='center', va='center', transform=plt.gca().transAxes)
        plt.title('Cantidad de Vistas por Género')

    buffer2 = io.BytesIO()
    plt.savefig(buffer2, format='png')
    buffer2.seek(0)
    plt.close()

    image_png2 = buffer2.getvalue()
    buffer2.close()
    graphic2 = base64.b64encode(image_png2)
    graphic2 = graphic2.decode('utf-8')

    return render(request, 'statistics.html', {'graphic1': graphic1, 'graphic2': graphic2})