from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q

from movies.models import FilmWork


# Общее поведение для всех API (QuerySet + JsonResponse)
class MoviesApiMixin:
    model = FilmWork
    http_method_names = ['get']

    # def get_queryset() возращает подготовленный QuerySet, где: 
    # annotate -  добавляет к полям модели дополнительные значения
    # Postgres-функция ArrayAgg собирает в список все значения, которые есть у поля
    # метод values превращает QuerySet в словарь
    def get_queryset(self):
        return (
            FilmWork.objects.values(
                'id', 'title', 'description', 'creation_date', 'rating', 'type'
            ).annotate(
                genres=ArrayAgg('genres__name', distinct=True),
                # для тестов persons разделяется
                actors=ArrayAgg(
                    'persons__full_name',
                    filter=Q(personfilmwork__role='actor'),
                    distinct=True
                ),
                directors=ArrayAgg(
                    'persons__full_name',
                    filter=Q(personfilmwork__role='director'),
                    distinct=True
                ),
                writers=ArrayAgg(
                    'persons__full_name',
                    filter=Q(personfilmwork__role='writer'),
                    distinct=True
                ),
            )
        )

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


# Список фильмов с постраничной разбивкой
class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, self.paginate_by)

        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset),
        }
        return context


# Подробная информация об одном фильме по UUID
# class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
#     def get_context_data(self, **kwargs):
#         return self.get_object()
class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_queryset(self):
        return super().get_queryset()

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        obj = queryset.filter(id=self.kwargs.get('pk')).first()
        if obj is None:
            from django.http import Http404
            raise Http404('FilmWork not found')
        return obj

    def get_context_data(self, **kwargs):
        return self.get_object()