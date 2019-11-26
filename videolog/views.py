# -*- coding: utf-8 -*-
from . import models
# utils:
from django.db.models import Q
from django.views.generic import ListView, DetailView
from .models import (VideoCategory, VideoPeople, VideoKeywords)
from django.shortcuts import (render, get_object_or_404)
from django.urls import reverse
import operator
from functools import reduce

from random import shuffle
# ..
# Main Views for Video Log
# ---------------------------------------
# ..

class InicioEntriesList(ListView):
    model = models.VideoEntry
    template_name = 'videolog/inicio.html'
    context_object_name = 'entries'
    #paginate_by = 5 #10
    #paginate_orphans = 3
    def get_queryset(self):
        queryset = super(InicioEntriesList, self).get_queryset().filter(
            Q(is_published=True) | Q(author__isnull=False, author=self.request.user.id))
        return queryset.order_by('?')
        
class EntriesList(ListView):
    model = models.VideoEntry
    template_name = 'videolog/entries_list.html'
    context_object_name = 'entries'
    #paginate_by = 5 #10
    #paginate_orphans = 3
    def get_queryset(self):
        queryset = super(EntriesList, self).get_queryset().filter(
            Q(is_published=True) | Q(author__isnull=False, author=self.request.user.id))
        return queryset.order_by('is_published', '-published_timestamp')  # Put 'drafts' first.

class EntryDetail(DetailView):
    model = models.VideoEntry
    template_name = 'videolog/entry_detail.html'
    context_object_name = 'entry'
    slug_field = 'slug'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['entry_list'] = models.VideoEntry.objects.all()
        return context
    def get_queryset(self):
        return super(EntryDetail, self).get_queryset().filter(
            Q(is_published=True) | Q(author__isnull=False, author=self.request.user.id))

class CategoryList(ListView):
    model = models.VideoEntry
    template_name = 'videolog/entries_list.html'
    context_object_name = 'entries'
    #paginate_by = 5
    #paginate_orphans = 3
    def get_queryset(self):
        self.category = get_object_or_404(VideoCategory, slug=self.kwargs['category'])
        return models.VideoEntry.objects.filter(category=self.category)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

class PeopleList(ListView):
    model = models.VideoEntry
    template_name = 'videolog/entries_list.html'
    context_object_name = 'entries'
    paginate_by = 5
    paginate_orphans = 3
    def get_queryset(self):
        self.people = get_object_or_404(VideoPeople, slug=self.kwargs['people'])
        return models.VideoEntry.objects.filter(people=self.people)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['people'] = self.people
        return context

class KeywordList(ListView):
    model = models.VideoEntry
    template_name = 'videolog/entries_list.html'
    context_object_name = 'entries'
    paginate_by = 5
    paginate_orphans = 3
    def get_queryset(self):
        self.keyword = get_object_or_404(VideoKeywords, slug=self.kwargs['keyword'])
        return models.VideoEntry.objects.filter(keywords=self.keyword)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['keyword'] = self.keyword
        return context

class SearchEntries(EntriesList):

    def get_queryset(self):
        result = super(SearchEntries, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            self.query = query
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                    (Q(title__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                    (Q(description__icontains=q) for q in query_list))
            )
            self.query_len = len(result)
        return result
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query
        context['query_len'] = self.query_len
        return context

# ..
# djangoCMS Views for Video Log
# ---------------------------------------
# ..

