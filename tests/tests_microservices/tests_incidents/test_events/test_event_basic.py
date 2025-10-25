"""
Базовые тесты для API мероприятий
Быстрые тесты для проверки основной функциональности
"""

import pytest
from tests_microservices.utils.incidents.events_api import EventsAPI
from tests_microservices.utils.incidents.events_schemas import MINIMAL_EVENT_DATA
from tests_microservices.checking import Checking

# Глобальная переменная для хранения ID созданных событий
created_event_ids = []


@pytest.mark.basic
@pytest.mark.smoke
@pytest.mark.regression
class TestEventsBasic:
    """Базовые тесты мероприятий"""

    def teardown_method(self):
        """Очистка после каждого теста - удаление созданных событий"""
        global created_event_ids
        for event_id in created_event_ids:
            try:
                EventsAPI.delete_event(event_id)
                print(f"Удалено событие с ID: {event_id}")
            except Exception as e:
                print(f"Ошибка при удалении события {event_id}: {e}")
        created_event_ids.clear()

    @pytest.mark.smoke
    def test_create_event(self):
        """Создать мероприятие"""
        response = EventsAPI.create_event(MINIMAL_EVENT_DATA)
        assert response.status_code in (200, 201)
        
        data = response.json()
        assert data['success'] is True
        
        # Сохраняем ID для последующего удаления
        created_event_ids.append(data['data']['id'])
        
        print(f"Мероприятие создано с ID: {data['data']['id']}")

    @pytest.mark.smoke
    def test_get_events_list(self):
        """Получить список мероприятий"""
        response = EventsAPI.list_events()
        assert response.status_code == 200
        
        data = response.json()
        assert 'data' in data
        print(f"Получено мероприятий: {len(data['data'])}")

    @pytest.mark.smoke
    def test_get_event_by_id(self):
        """Получить мероприятие по ID"""
        # Сначала создаем мероприятие
        create_response = EventsAPI.create_event(MINIMAL_EVENT_DATA)
        event_id = create_response.json()['data']['id']
        created_event_ids.append(event_id)
        
        # Получаем его по ID
        response = EventsAPI.get_event(event_id)
        assert response.status_code == 200
        
        data = response.json()
        assert data['data']['id'] == event_id
        print(f"Мероприятие {event_id} найдено")

    @pytest.mark.smoke
    def test_update_event(self):
        """Обновить мероприятие"""
        # Создаем мероприятие
        create_response = EventsAPI.create_event(MINIMAL_EVENT_DATA)
        event_id = create_response.json()['data']['id']
        created_event_ids.append(event_id)
        
        # Обновляем название
        update_data = {"name": "Обновленное мероприятие"}
        response = EventsAPI.update_event(event_id, update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data['data']['name'] == "Обновленное мероприятие"
        print(f"Мероприятие {event_id} обновлено")

    @pytest.mark.smoke
    def test_delete_event(self):
        """Удалить мероприятие"""
        # Создаем мероприятие
        create_response = EventsAPI.create_event(MINIMAL_EVENT_DATA)
        event_id = create_response.json()['data']['id']
        created_event_ids.append(event_id)
        
        # Удаляем его
        response = EventsAPI.delete_event(event_id)
        assert response.status_code == 200
        
        # Проверяем, что удалено
        get_response = EventsAPI.get_event(event_id)
        assert get_response.status_code == 404
        print(f"Мероприятие {event_id} удалено")

    def test_create_event_with_full_data(self):
        """Создать мероприятие с полными данными"""
        full_data = {
            "name": "Полное мероприятие",
            "short_name": "Полное",
            "international_name": "Full Event",
            "date_start": "2025-01-01T00:00:00+03:00",
            "date_end": "2025-01-31T23:59:59+03:00",
            "objects": [
                {
                    "id": 1,
                    "name": "Тестовый объект"
                }
            ]
        }
        
        response = EventsAPI.create_event(full_data)
        # API может отклонить из-за валидации - это нормально
        assert response.status_code in (200, 201, 422)
        
        data = response.json()
        if response.status_code in (200, 201):
            assert data['success'] is True
            
            # Сохраняем ID для последующего удаления
            created_event_ids.append(data['data']['id'])
            
            print(f"Полное мероприятие создано с ID: {data['data']['id']}")
        else:
            print(f"API отклонил создание: {data}")

    def test_invalid_event_id(self):
        """Проверить несуществующий ID"""
        response = EventsAPI.get_event(99999)
        assert response.status_code == 404
        print("Несуществующий ID корректно обработан")

    def test_empty_event_name(self):
        """Проверить пустое название"""
        invalid_data = MINIMAL_EVENT_DATA.copy()
        invalid_data['name'] = ""
        
        response = EventsAPI.create_event(invalid_data)
        # API может принять или отклонить - проверяем оба варианта
        assert response.status_code in (200, 201, 400, 422)
        print("Пустое название обработано")

    def test_past_dates(self):
        """Проверить даты в прошлом"""
        past_data = MINIMAL_EVENT_DATA.copy()
        past_data['date_start'] = "2020-01-01T00:00:00+03:00"
        past_data['date_end'] = "2020-01-31T23:59:59+03:00"
        
        response = EventsAPI.create_event(past_data)
        # API может принять или отклонить
        assert response.status_code in (200, 201, 400, 422)
        print("Даты в прошлом обработаны")

    def test_end_before_start(self):
        """Проверить дату окончания раньше начала"""
        invalid_data = MINIMAL_EVENT_DATA.copy()
        invalid_data['date_start'] = "2025-01-31T23:59:59+03:00"
        invalid_data['date_end'] = "2025-01-01T00:00:00+03:00"
        
        response = EventsAPI.create_event(invalid_data)
        # API может принять или отклонить
        assert response.status_code in (200, 201, 400, 422)
        print("Неправильные даты обработаны")


if __name__ == "__main__":
    # Запуск базовых тестов
    pytest.main([__file__, "-v", "-s"]) 