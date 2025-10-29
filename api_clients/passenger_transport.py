#!/usr/bin/env python3
"""
API клиент для раздела Пассажирский транспорт
"""

import os
import requests


class PassengerTransportAPIClient:
    def __init__(self):
        self.base_url = "http://91.227.17.139/services/transport-passenger/api"
        self.report_url = "http://91.227.17.139/services/report/api/v2/report/request"
        self.token = self._get_token()
        self.headers = self._get_headers()

    def _get_token(self):
        token = os.getenv("API_TOKEN")
        if not token:
            raise ValueError("Токен не найден! Запустите refresh_token.py")
        return token

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "project": "98_spb",
            "Accept": "application/json, text/plain, */*"
        }

    def check_token(self):
        """Проверяет валидность токена"""
        try:
            response = requests.get(f"{self.base_url}/station", headers=self.headers, params={"page": 1, "limit": 1}, verify=False, timeout=10)
            if response.status_code == 200:
                return True
            elif response.status_code == 401:
                return False
            return False
        except requests.exceptions.RequestException:
            return False

    # ========== ROUTES (Маршруты) ==========
    def get_routes_list(self, page=1, limit=25, status_list=None):
        """Получить список маршрутов"""
        url = f"{self.base_url}/route/grouped"
        params = {"page": page, "limit": limit}
        if status_list:
            for status in status_list:
                params[f"status_list[]"] = status
        return requests.get(url, headers=self.headers, params=params, verify=False)

    def get_trans_organizations_list(self, page=1, limit=25):
        """Получить список привязки организаций"""
        url = f"{self.base_url}/trans-organization"
        params = {"page": page, "limit": limit}
        return requests.get(url, headers=self.headers, params=params, verify=False)

    # ========== STATIONS (Остановки) ==========
    def get_stations_list(self, page=1, limit=25):
        """Получить список остановок"""
        url = f"{self.base_url}/station"
        params = {"page": page, "limit": limit}
        return requests.get(url, headers=self.headers, params=params, verify=False)

    def create_station(self, name, direction, comment, attribute, type_list, view, organization_id, check_point):
        """Создать остановку"""
        url = f"{self.base_url}/station/"
        payload = {
            "name": name,
            "direction": direction,
            "comment": comment,
            "attribute": attribute,
            "type_list": type_list,
            "view": view,
            "organization_id": organization_id,
            "check_point": check_point
        }
        return requests.post(url, headers=self.headers, json=payload, verify=False)

    def update_station(self, station_id, name, direction, comment, attribute, type_list, view, organization_id, check_point):
        """Обновить остановку"""
        url = f"{self.base_url}/station/{station_id}"
        payload = {
            "name": name,
            "direction": direction,
            "comment": comment,
            "attribute": attribute,
            "type_list": type_list,
            "view": view,
            "organization_id": organization_id,
            "check_point": check_point
        }
        return requests.put(url, headers=self.headers, json=payload, verify=False)

    def delete_station(self, station_id):
        """Удалить остановку"""
        url = f"{self.base_url}/station/{station_id}"
        return requests.delete(url, headers=self.headers, verify=False)

    # ========== VEHICLES (Транспортные средства) ==========
    def get_vehicles_list(self, page=1, limit=25):
        """Получить список ТС"""
        url = f"{self.base_url}/vehicle"
        params = {"page": page, "limit": limit}
        return requests.get(url, headers=self.headers, params=params, verify=False)

    def create_vehicle(self, number, garage_number, model_id, category_id, class_id, characteristics, organization_id):
        """Создать ТС"""
        url = f"{self.base_url}/vehicle"
        payload = {
            "number": number,
            "garage_number": garage_number,
            "model_id": model_id,
            "category_id": category_id,
            "class_id": class_id,
            "characteristics": characteristics,
            "organization_id": organization_id
        }
        return requests.post(url, headers=self.headers, json=payload, verify=False)

    def update_vehicle(self, vehicle_id, number, garage_number, model_id, category_id, class_id, characteristics, organization_id):
        """Обновить ТС"""
        url = f"{self.base_url}/vehicle/{vehicle_id}"
        payload = {
            "number": number,
            "garage_number": garage_number,
            "model_id": model_id,
            "category_id": category_id,
            "class_id": class_id,
            "characteristics": characteristics,
            "organization_id": organization_id
        }
        return requests.put(url, headers=self.headers, json=payload, verify=False)

    def delete_vehicle(self, vehicle_id):
        """Удалить ТС"""
        url = f"{self.base_url}/vehicle/{vehicle_id}"
        return requests.delete(url, headers=self.headers, verify=False)

    def get_vehicle_card(self, vehicle_id):
        """Получить учетную карточку ТС"""
        url = f"{self.base_url}/vehicle/{vehicle_id}/card"
        return requests.get(url, headers=self.headers, verify=False)

    def get_vehicle_history(self, vehicle_id, date_start, date_end):
        """Получить историю перемещений ТС"""
        url = f"{self.base_url}/vehicle/history/{vehicle_id}"
        params = {"date_start": date_start, "date_end": date_end}
        return requests.get(url, headers=self.headers, params=params, verify=False)

    def generate_vehicle_report(self, vehicle_id, start_date, end_date, formats):
        """Сгенерировать отчет по ТС"""
        url = f"{self.report_url}/13"
        payload = {
            "vehicle_id": vehicle_id,
            "start_date": start_date,
            "end_date": end_date,
            "formats": formats
        }
        return requests.post(url, headers=self.headers, json=payload, verify=False)

    # ========== BRANDS (Марки) ==========
    def get_brands_list(self, page=1, limit=25):
        """Получить список марок"""
        url = f"{self.base_url}/brand"
        params = {"page": page, "limit": limit}
        return requests.get(url, headers=self.headers, params=params, verify=False)

    def create_brand(self, name_ru, name_en, slug, category_id):
        """Создать марку"""
        url = f"{self.base_url}/brand"
        payload = {
            "name_ru": name_ru,
            "name_en": name_en,
            "slug": slug,
            "category_id": category_id
        }
        return requests.post(url, headers=self.headers, json=payload, verify=False)

    def update_brand(self, brand_id, name_ru, name_en, slug, category_id):
        """Обновить марку"""
        url = f"{self.base_url}/brand/{brand_id}"
        payload = {
            "name_ru": name_ru,
            "name_en": name_en,
            "slug": slug,
            "category_id": category_id
        }
        return requests.put(url, headers=self.headers, json=payload, verify=False)

    def delete_brand(self, brand_id):
        """Удалить марку"""
        url = f"{self.base_url}/brand/{brand_id}"
        return requests.delete(url, headers=self.headers, verify=False)

    # ========== MODELS (Модели) ==========
    def get_models_list(self, page=1, limit=25):
        """Получить список моделей"""
        url = f"{self.base_url}/model"
        params = {"page": page, "limit": limit}
        return requests.get(url, headers=self.headers, params=params, verify=False)

    def create_model(self, brand_id, name_ru, name_en, slug):
        """Создать модель"""
        url = f"{self.base_url}/model"
        payload = {
            "brand_id": brand_id,
            "name_ru": name_ru,
            "name_en": name_en,
            "slug": slug
        }
        return requests.post(url, headers=self.headers, json=payload, verify=False)

    def update_model(self, model_id, brand_id, name_ru, name_en, slug):
        """Обновить модель"""
        url = f"{self.base_url}/model/{model_id}"
        payload = {
            "brand_id": brand_id,
            "name_ru": name_ru,
            "name_en": name_en,
            "slug": slug
        }
        return requests.put(url, headers=self.headers, json=payload, verify=False)

    def delete_model(self, model_id):
        """Удалить модель"""
        url = f"{self.base_url}/model/{model_id}"
        return requests.delete(url, headers=self.headers, verify=False)


