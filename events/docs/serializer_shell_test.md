# Test serializatora EventSerializer w powłoce Django

Wyniki wygenerowane poleceniem `python manage.py serializer_shell_test` (kod wykonywany jak w `python manage.py shell`).

## 1. Serializacja: obiekt Event -> słownik -> JSON

```python
import io
from events.models import Event
from events.serializers import EventSerializer
from rest_framework.renderers import JSONRenderer

event = Event.objects.first()
serializer = EventSerializer(event)
print(serializer.data)
json_bytes = JSONRenderer().render(serializer.data)
print(json_bytes)
```

Wynik:

```text
{'id': 2, 'title': 'Meetup Python Olsztyn', 'slug': 'meetup-python-olsztyn', 'category_id': 1, 'organizer_id': 1, 'description': 'Otwarte spotkanie społeczności Pythona. Lightning talki i networking.', 'location': 'Olsztyn, Browar Dziki', 'date': '2026-11-03T18:00:00+01:00', 'capacity': 60, 'price': '0.00', 'is_published': True, 'created_at': '2026-10-27T18:34:15.541814+01:00'}
b'{"id":2,"title":"Meetup Python Olsztyn","slug":"meetup-python-olsztyn","category_id":1,"organizer_id":1,"description":"Otwarte spotkanie spo\xc5\x82eczno\xc5\x9bci Pythona. Lightning talki i networking.","location":"Olsztyn, Browar Dziki","date":"2026-11-03T18:00:00+01:00","capacity":60,"price":"0.00","is_published":true,"created_at":"2026-10-27T18:34:15.541814+01:00"}'
```

## 2. Deserializacja: JSON -> słownik -> nowy Event w bazie

```python
from rest_framework.parsers import JSONParser

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
    print("Błędy walidacji:", deserializer.errors)
```

Wynik:

```text
Dane są poprawne!
{'title': 'Nowe Warsztaty Pythona', 'slug': 'nowe-warsztaty-pythona', 'category': <Category: Technologia>, 'organizer': <User: admin>, 'description': 'Otwarte spotkanie społeczności Pythona. Lightning talki i networking.', 'location': 'Olsztyn, Browar Dziki', 'date': datetime.datetime(2026, 11, 3, 18, 0, tzinfo=zoneinfo.ZoneInfo(key='Europe/Warsaw')), 'capacity': 60, 'price': Decimal('0.00'), 'is_published': True}
Utworzono wydarzenie o id=6
```

## 3. Błędne dane: pusty tytuł i ujemny limit miejsc

```python
invalid_data = {'title': '', 'capacity': -5}
bad_serializer = EventSerializer(data=invalid_data)
print("Czy poprawne?", bad_serializer.is_valid())
print("Błędy:", bad_serializer.errors)
```

Wynik:

```text
Czy poprawne? False
Błędy: {'title': [ErrorDetail(string='To pole nie może być puste.', code='blank')], 'slug': [ErrorDetail(string='To pole jest wymagane.', code='required')], 'category_id': [ErrorDetail(string='To pole jest wymagane.', code='required')], 'organizer_id': [ErrorDetail(string='To pole jest wymagane.', code='required')], 'description': [ErrorDetail(string='To pole jest wymagane.', code='required')], 'location': [ErrorDetail(string='To pole jest wymagane.', code='required')], 'date': [ErrorDetail(string='To pole jest wymagane.', code='required')], 'capacity': [ErrorDetail(string='Upewnij się, że ta wartość jest większa lub równa 1.', code='min_value')]}
```

## 4. Błędne dane: brak kategorii i niepoprawny format daty

```python
invalid_data_2 = {
    'title': 'Test', 'slug': 'test', 'organizer_id': 1,
    'description': 'Opis', 'location': 'Olsztyn',
    'date': 'to-nie-jest-data', 'capacity': 10,
}
bad_serializer_2 = EventSerializer(data=invalid_data_2)
print("Czy poprawne?", bad_serializer_2.is_valid())
print("Błędy:", bad_serializer_2.errors)
```

Wynik:

```text
Czy poprawne? False
Błędy: {'category_id': [ErrorDetail(string='To pole jest wymagane.', code='required')], 'date': [ErrorDetail(string='Wartość daty z czasem ma zły format. Użyj jednego z dostępnych formatów: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].', code='invalid')]}
```
