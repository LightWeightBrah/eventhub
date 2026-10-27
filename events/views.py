from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Event, Category


# --- Lab 1: pierwsze widoki funkcyjne ---

def welcome_view(request):
    return HttpResponse("Witaj w platformie EventHub – systemie obsługi wydarzeń i biletów!")


def about_view(request):
    """Krótki opis funkcjonalności platformy EventHub."""
    return HttpResponse(
        "EventHub to platforma do zarządzania wydarzeniami (konferencjami, warsztatami, "
        "koncertami). Umożliwia tworzenie wydarzeń, zakup biletów oraz wystawianie ocen."
    )


# --- Lab 3: widoki MVT z szablonami ---

def event_list(request):
    """Widok listy opublikowanych wydarzeń z wyszukiwarką (?q=...)."""
    events = Event.objects.filter(is_published=True).select_related('category', 'organizer')

    q = request.GET.get('q', '').strip()
    if q:
        events = events.filter(title__icontains=q)

    return render(request, 'events/event_list.html', {
        'events': events,
        'categories': Category.objects.all(),
        'current_category': None,
        'q': q,
    })


def event_detail(request, slug):
    """Widok pojedynczego wydarzenia na podstawie parametru slug."""
    event = get_object_or_404(
        Event.objects.select_related('category', 'organizer'),
        slug=slug,
        is_published=True
    )
    related_events = (
        Event.objects
        .filter(category=event.category, is_published=True)
        .exclude(id=event.id)
        .select_related('category')[:3]
    )
    return render(request, 'events/event_detail.html', {
        'event': event,
        'related_events': related_events,
    })


def events_by_category(request, category_slug):
    """Wydarzenia przefiltrowane według kategorii."""
    category = get_object_or_404(Category, slug=category_slug)
    events = category.events.filter(is_published=True).select_related('category', 'organizer')
    return render(request, 'events/event_list.html', {
        'events': events,
        'categories': Category.objects.all(),
        'current_category': category,
        'q': '',
    })
