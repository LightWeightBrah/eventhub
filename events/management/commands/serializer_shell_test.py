"""
Lab 4, zadanie 3 - generuje plik events/docs/serializer_shell_test.md
z PRAWDZIWYMI wynikami serializacji, deserializacji i walidacji.

Użycie (po `python manage.py seed_demo`):
    python manage.py serializer_shell_test
"""
import contextlib
import io
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from events.models import Event

SLUG = 'nowe-warsztaty-pythona'

STEPS = [
    (
        "1. Serializacja: obiekt Event -> słownik -> JSON",
        '''import io
from events.models import Event
from events.serializers import EventSerializer
from rest_framework.renderers import JSONRenderer

event = Event.objects.first()
serializer = EventSerializer(event)
print(serializer.data)
json_bytes = JSONRenderer().render(serializer.data)
print(json_bytes)''',
    ),
    (
        "2. Deserializacja: JSON -> słownik -> nowy Event w bazie",
        '''from rest_framework.parsers import JSONParser

stream = io.BytesIO(json_bytes)
data = JSONParser().parse(stream)
data['title'] = "Nowe Warsztaty Pythona"
data['slug'] = "nowe-warsztaty-pythona"

deserializer = EventSerializer(data=data)
if deserializer.is_valid():
    print("Dane są poprawne!")
    print(deserializer.validated_data)
    new_event = deserializer.save()
    print(f"Utworzono wydarzenie o id={new_event.id}")
else:
    print("Błędy walidacji:", deserializer.errors)''',
    ),
    (
        "3. Błędne dane: pusty tytuł i ujemny limit miejsc",
        '''invalid_data = {'title': '', 'capacity': -5}
bad_serializer = EventSerializer(data=invalid_data)
print("Czy poprawne?", bad_serializer.is_valid())
print("Błędy:", bad_serializer.errors)''',
    ),
    (
        "4. Błędne dane: brak kategorii i niepoprawny format daty",
        '''invalid_data_2 = {
    'title': 'Test', 'slug': 'test', 'organizer_id': 1,
    'description': 'Opis', 'location': 'Olsztyn',
    'date': 'to-nie-jest-data', 'capacity': 10,
}
bad_serializer_2 = EventSerializer(data=invalid_data_2)
print("Czy poprawne?", bad_serializer_2.is_valid())
print("Błędy:", bad_serializer_2.errors)''',
    ),
]


class Command(BaseCommand):
    help = "Generuje events/docs/serializer_shell_test.md z rzeczywistymi wynikami."

    def handle(self, *args, **options):
        if not Event.objects.exists():
            raise CommandError("Brak wydarzeń w bazie. Najpierw: python manage.py seed_demo")

        # Powtarzalność: usuwamy wydarzenie utworzone przy poprzednim uruchomieniu.
        Event.objects.filter(slug=SLUG).delete()

        namespace = {}
        lines = [
            "# Test serializatora EventSerializer w powłoce Django",
            "",
            "Wyniki wygenerowane poleceniem `python manage.py serializer_shell_test` "
            "(kod wykonywany jak w `python manage.py shell`).",
            "",
        ]
        for title, code in STEPS:
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                exec(code, namespace)
            lines += [
                f"## {title}",
                "",
                "```python",
                code,
                "```",
                "",
                "Wynik:",
                "",
                "```text",
                buffer.getvalue().rstrip(),
                "```",
                "",
            ]

        target = Path(__file__).resolve().parents[2] / 'docs' / 'serializer_shell_test.md'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("\n".join(lines), encoding='utf-8')
        self.stdout.write(self.style.SUCCESS(f"Zapisano: {target}"))
