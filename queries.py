# queries.py
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema.settings')
django.setup()

from movies.models import Genre, Director, Movie, Review
from django.db.models import Count, Avg, Min, Max, Q, F
# Всі фільми (повні об'єкти)
movies = Movie.objects.all()

# Тільки назви — flat=True повертає список рядків, не кортежів
titles = Movie.objects.values_list("title", flat=True)
print(list(titles))
# Результат ['The Dark Knight', 'Pulp Fiction', 'Inception', 'Interstellar', 'Django Unchained', 'Parasite', 'Inglourious Basterds', 'The Grand Budapest Hotel', 'Dune', 'Blade Runner 2049', 'Arrival', 'Tenet']


top_movies = Movie.objects.filter(rating__gte=8.5).order_by("-rating")
for m in top_movies:
    print(m.title, m.rating)
# Результат
# The Dark Knight 9.0
# Pulp Fiction 8.9
# Inception 8.8
# Interstellar 8.6
# Django Unchained 8.5
# Parasite 8.5

from django.db.models import Q

result = Movie.objects.filter(
    Q(title__icontains="Blade") | Q(title__icontains="Dark")
)
print(result)
# Результат [<Movie: The Dark Knight (2008)>, <Movie: Blade Runner 2049 (2017)>]>

nolan_films = Movie.objects.filter(director__last_name="Nolan")
print(nolan_films)
# Результат [<Movie: The Dark Knight (2008)>, <Movie: Inception (2010)>, <Movie: Interstellar (2014)>, <Movie: Tenet (2020)>

scifi_modern = Movie.objects.filter(
    genre__name="Sci-Fi",
    year__gt=2015
).order_by("year")
print("Завдання 5:")
for m in scifi_modern:
    print(f"- {m.title} ({m.year})")
print(scifi_modern)
print( list(Movie.objects.filter(year__gt=2015).values_list('title', 'year')))
# Результат[('Parasite', 2019), ('Dune', 2021), ('Blade Runner 2049', 2017), ('Arrival', 2016), ('Tenet', 2020)]

result = Movie.objects.exclude(
    Q(genre__name="Drama") | Q(genre__name="Comedy")
)
for m in result:
    print(m.title, "—", m.genre.name if m.genre else "без жанру")
# Результат The Dark Knight — Thriller
# Pulp Fiction — Crime
# Inception — Sci-Fi
# Django Unchained — Crime
# Parasite — Crime
# Inglourious Basterds — Sci-Fi
# Tenet — Thriller



by_rating = Movie.objects.order_by("-rating")


page1 = by_rating[:4]
print("Завдання 7, Сторінка 1:")
for m in page1:
    print(f"- {m.title} ({m.rating})")

page2 = by_rating[4:8]
print("\nЗавдання 7, Сторінка 2:")
for m in page2:
    print(f"- {m.title} ({m.rating})")

# Результат Завдання 7, Сторінка 1:
# - The Dark Knight (9.0)
# - Pulp Fiction (8.9)
# - Inception (8.8)
# - Interstellar (8.6)
#
# Завдання 7, Сторінка 2:
# - Django Unchained (8.5)
# - Parasite (8.5)
# - Inglourious Basterds (8.3)
# - The Grand Budapest Hotel (8.1)


from django.db.models import Count

genres = Genre.objects.annotate(
    movie_count=Count("movie")
).order_by("-movie_count")

for g in genres:
    print(g.name, ":", g.movie_count)
# Результат
#Drama : 4
#Crime : 3
#Sci-Fi : 2
#Thriller : 2
#Comedy : 1
#Comedy : 0
#Thriller : 0
#Drama : 0
#Crime : 0

from django.db.models import Avg

# Загальний середній
total_avg = Movie.objects.aggregate(avg=Avg("rating"))
print("Середнiй рейтинг:", total_avg["avg"])

# По режисерах
directors = Director.objects.annotate(
    avg_rating=Avg("movie__rating")
).values("last_name", "avg_rating").order_by("-avg_rating")

for d in directors:
    print(d["last_name"], ":", d["avg_rating"])
# Результат Середнiй рейтинг: 8.3333333333333333
# Tarantino : 8.5666666666666667
# Joon-ho : 8.5000000000000000
# Nolan : 8.4500000000000000
# Anderson : 8.1000000000000000
# Villeneuve : 7.9666666666666667


no_reviews = Movie.objects.filter(review__isnull=True)
for m in no_reviews:
    print(f"- {m.title}")

# - The Dark Knight
# - Pulp Fiction
# - Interstellar
# - Django Unchained
# - Inglourious Basterds
# - The Grand Budapest Hotel
# - Dune
# - Blade Runner 2049
# - Arrival


no_reviews_v2= Movie.objects.annotate(
    review_count=Count("review")
).filter(review_count=0)

for m in no_reviews_v2:
    print(f"- {m.title}  {m.review_count})")

# - Arrival  0)
# - The Dark Knight  0)
# - Pulp Fiction  0)
# - Blade Runner 2049  0)
# - Inglourious Basterds  0)
# - Interstellar  0)
# - Django Unchained 0)
# - The Grand Budapest Hotel  0)
# - Dune  0)

updated_count = Movie.objects.filter(rating__lt=7.8).update(is_public=False)
print(f"Оновлено: {updated_count} фiльмiв")
# Оновлено: 1 фiльмiв

from django.db.models import F

Movie.objects.filter(
    director__last_name="Tarantino"
).update(rating=F("rating") + 0.2)
print(f"Завдання 9: Оновлено фільмів: {updated_count}")
tarantino_movies = Movie.objects.filter(director__last_name="Tarantino")
for m in tarantino_movies:
    print(f"- {m.title}: новий рейтинг {m.rating}")
# Оновлено: 1 фiльмiв
# Завдання 9: Оновлено фільмів: 1
# - Pulp Fiction: новий рейтинг 9.5
# - Django Unchained: новий рейтинг 9.1
# - Inglourious Basterds: новий рейтинг 8.9


inception = Movie.objects.get(title="Inception")

# Зворотній ForeignKey — review_set
reviews = inception.review_set.all()
for r in reviews:
    print(r.score, ":", r.text)

# Середня оцінка
avg_score = inception.review_set.aggregate(avg=Avg("score"))
print("Середня оцiнка:", avg_score["avg"])
# 10 : Складно але геніально.
# 9 : Дивився тричi, кожен раз нове.
# Середня оцiнка: 9.5

best_director = Director.objects.annotate(
    avg_rating=Avg("movie__rating")
).order_by("-avg_rating").first()


if best_director:
    print(f"Найкращий режисер: {best_director.first_name} {best_director.last_name}")
    print(f"Середній рейтинг фільмів: {best_director.avg_rating:.2f}")
else:
    print("Режисерів не знайдено.")
# Найкращий режисер: Quentin Tarantino
# Середній рейтинг фільмів: 9.77

nolan_bad_reviews_count = Review.objects.filter(
    movie__director__last_name="Nolan",
    score__lt=7
).count()

print(f"Кількість критичних відгуків на фільми Нолана: {nolan_bad_reviews_count}")
# Цей ORM-запит рахує кількість відгуків з низькою оцінкою
# Кількість критичних відгуків на фільми Нолана: 1