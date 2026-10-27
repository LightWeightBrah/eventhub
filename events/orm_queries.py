"""
Lab 2 - zapytania QuerySet na modelach EventHub.

Uruchomienie (z głównego folderu projektu, przy aktywnym .venv):
    python -m events.orm_queries
"""
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventhub.settings')
django.setup()

from events.models import Event  # noqa: E402  (import po django.setup())


def main():
    # 1. Wszystkie opublikowane wydarzenia posortowane chronologicznie
    print("1. Opublikowane wydarzenia (chronologicznie):")
    published = Event.objects.filter(is_published=True).order_by('date')
    for event in published:
        print(f"   - {event.date:%Y-%m-%d %H:%M}  {event.title}")

    # 2. Wydarzenia z limitem miejsc co najmniej 50
    print("\n2. Wydarzenia z limitem miejsc >= 50:")
    big_events = Event.objects.filter(capacity__gte=50)
    for event in big_events:
        print(f"   - {event.title} (limit: {event.capacity})")

    # 3. Łączna liczba darmowych wydarzeń
    free_count = Event.objects.filter(price=0.00).count()
    print(f"\n3. Liczba darmowych wydarzeń: {free_count}")

    # 4. Zmiana statusu is_published z True na False i zapis w bazie
    event = Event.objects.filter(is_published=True).first()
    if event is None:
        print("\n4. Brak opublikowanych wydarzeń do zmiany statusu.")
        return
    print(f"\n4. Zmieniam status wydarzenia '{event.title}'")
    event.is_published = False
    event.save()
    event.refresh_from_db()
    print(f"   is_published po zapisie: {event.is_published}")

    # Przywracamy status, żeby dane demo pozostały kompletne.
    event.is_published = True
    event.save()
    print("   Status przywrócony na True.")


if __name__ == '__main__':
    main()
