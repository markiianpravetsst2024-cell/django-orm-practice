from django.db import models

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']
class Director(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_year = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
class Movie(models.Model):
    title = models.CharField(max_length=300)
    year = models.IntegerField()
    rating = models.    DecimalField(max_digits=3, decimal_places=1)
    duration = models.IntegerField(help_text='Тривалість у хвилинах')
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    director = models.ForeignKey(
        Director, on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.title} ({self.year})'

    class Meta:
        ordering = ['-rating']


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    text = models.TextField()
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Вiдгук на {self.movie.title} — {self.score}/10'