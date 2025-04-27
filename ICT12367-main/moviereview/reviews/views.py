from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import JsonResponse
from .models import Movie
from .forms import ReviewForm, MovieForm

def movie_list(request):
    query = request.GET.get('q')  # รับค่าค้นหาจาก query string
    if query:
        movies = Movie.objects.filter(Q(title__icontains=query))
    else:
        movies = Movie.objects.all()
    return render(request, 'reviews/movie_list.html', {'movies': movies})

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.save()
            return redirect('movie_detail', pk=movie.pk)
    else:
        form = ReviewForm()
    return render(request, 'reviews/movie_detail.html', {'movie': movie, 'form': form})

def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('movie_list')
    else:
        form = MovieForm()
    return render(request, 'reviews/add_movie.html', {'form': form})

# ✅ autocomplete view
def autocomplete_movies(request):
    term = request.GET.get('term', '')
    movie_titles = list(Movie.objects.filter(title__icontains=term).values_list('title', flat=True)[:10])
    return JsonResponse(movie_titles, safe=False)
