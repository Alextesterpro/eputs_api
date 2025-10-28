"""
API клиент для работы с Водным транспортом
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()


class WaterTransportAPIClient:
    """Клиент для работы с API Водного транспорта"""

    def __init__(self):
        self.base_url = "http://91.227.17.139/services/transport-water/api"
        self.token = self._get_token()
        self.headers = self._get_headers()

    def _get_token(self):
        """Получение токена из .env файла"""
        token = os.getenv("API_TOKEN")
        if not token:
            raise ValueError("Токен не найден! Запустите update_token.py")
        return token

    def _get_headers(self):
        """Получение заголовков для запросов"""
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "project": "98_spb"
        }

    def check_token(self):
        """Проверка валидности токена"""
        try:
            response = self.vehicle_list(page=1, limit=1)
            return response.status_code != 401
        except Exception:
            return False

    # ==================== CRUD для транспортных средств ====================

    def vehicle_list(self, page: int = 1, limit: int = 25):
        """
        Получение списка транспортных средств
        
        Args:
            page: номер страницы
            limit: количество элементов на странице
        """
        url = f"{self.base_url}/vehicle/list"
        payload = {
            "page": page,
            "limit": limit
        }
        return requests.post(url, json=payload, headers=self.headers)

    def vehicle_create(self, name: str, short_name: str, mmsi: str, imo: str, vehicle_type: str = "5"):
        """
        Создание транспортного средства
        
        Args:
            name: название
            short_name: короткое название
            mmsi: MMSI номер (9 цифр)
            imo: IMO номер (7 цифр)
            vehicle_type: тип транспорта (по умолчанию "5")
        """
        url = f"{self.base_url}/vehicle"
        payload = {
            "name": name,
            "short_name": short_name,
            "mmsi": mmsi,
            "imo": imo,
            "type": vehicle_type
        }
        return requests.post(url, json=payload, headers=self.headers)

    def vehicle_update(self, vehicle_id: int, name: str, short_name: str, mmsi: str, imo: str, vehicle_type: str = "5"):
        """
        Обновление транспортного средства
        
        Args:
            vehicle_id: ID транспортного средства
            name: название
            short_name: короткое название
            mmsi: MMSI номер (9 цифр)
            imo: IMO номер (7 цифр)
            vehicle_type: тип транспорта
        """
        url = f"{self.base_url}/vehicle/{vehicle_id}"
        payload = {
            "name": name,
            "short_name": short_name,
            "mmsi": mmsi,
            "imo": imo,
            "type": vehicle_type
        }
        return requests.put(url, json=payload, headers=self.headers)

    def vehicle_delete(self, vehicle_id: int):
        """
        Удаление транспортного средства
        
        Args:
            vehicle_id: ID транспортного средства
        """
        url = f"{self.base_url}/vehicle/{vehicle_id}"
        return requests.delete(url, headers=self.headers)

