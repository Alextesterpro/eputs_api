import requests
from typing import Dict, Any, Optional, List
from datetime import datetime

class TransportAPI:
    """API для работы с пассажирским транспортом"""
    
    # Базовый URL API
    BASE_URL = "http://91.227.17.139/services/transport-passenger/api"
    
    # Общие заголовки для всех запросов
    HEADERS = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiNDk2ZThhNzliZjQ1Y2NjYjNkNTk5YzAzYzQ5ZTU4NTJkYjM4MjUwZjVmZTQwYTAwMWM0YzEzNDI2YWEyMTVhZDQ4ZjRlZjczZWE0YjExMWQiLCJpYXQiOjE3NDU4NDAzMDMuNTkyMzU5LCJuYmYiOjE3NDU4NDAzMDMuNTkyNTc4LCJleHAiOjE3NDcxMzYzMDMuMjgwNzkzLCJzdWIiOiIyNCIsInNjb3BlcyI6W10sIm9yZ2FuaXphdGlvbl9pZF9saXN0IjpbXSwiaWRlbnRpZmllciI6ImEudmVzZWxvdl9BQUFfZm9ybWF0dHdvLnJ1XzE3MjQ3NDYzNjYuMzQ2MyIsImVtYWlsIjoiYS52ZXNlbG92QGZvcm1hdHR3by5ydSIsInVzZXJfbmFtZSI6ImEudmVzZWxvdkBmb3JtYXR0d28ucnUiLCJmaXJzdF9uYW1lIjoi0JDQu9C10LrRgdCw0L3QtNGAIiwibGFzdF9uYW1lIjoi0JLQtdGB0LXQu9C-0LIiLCJtaWRkbGVfbmFtZSI6ItCS0LjQutGC0L7RgNC-0LLQuNGHIn0.ZedrGIbjgnH28rDsvqtEyQbsZ5RFTH-kLIVZXP0qLxk7hXdjRcpbAtMr9MRCbAxT6pi279lMnNT4vtwKqBMjr9M-3xh-XExrqlqeR_3Z5SMmZPTI8D4lYUhjmiHzuexIbr_JhKIXNHjQUdldLPlyd7V789wlv_x1rA4kb9RtvmdlUwO8LbxbJis-plNeRp80Fu59jDV1ZZhT48tfjiWLcS-Gaq7RucAAnG_k8zKH8uzCogmbKmGTSJDtr8VyPNC-3U6usIeCMGbgYnjlkyydFxZcQZ7NQGfsuHLPWmyqjO69mAl0hcIwFHEXWlXiczS-S-JjnfrW2d8GbbSmYwYvx8rfzz2gaw295kYcr-w6gykmJDW7_gM_KvBWB_mNWmLEvvtAkip1m7syGAuGP8sbaFuuQw02DEiZZaVDvESXq9SjLHxCcaprYnR_T3xaQVqS4Yrw4RMQfWduOFCBMcWlhH7DjCuxth3OIe810_N9GclfLa8y2h5cCKtoJNTGyYsMTn4EWd93XqtJFn71sjiM27xSN7nQZkF9Ep0ylfg_M50HslmagZqLygB7GzHTVjQyoBQfRmpym4zOnxbLSEbjdXy3idX6B2UfMp5IWY0BYdgGaXAdk0uyRPY6dFeCHqQrF9D22Kao1KaDz9am14QFobkhFa3iiPF4WOySb7Kj8dw",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Referer": "http://91.227.17.139/dictionaries/passenger-transport/stations",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "project": "98_spb",
        "service": "eputs",
        "Content-Type": "application/json"
    }
    
    @classmethod
    def create_route(cls, **data):
        """Создание нового маршрута с любым набором обязательных полей"""
        return requests.post(
            f"{cls.BASE_URL}/route",
            json=data,
            headers=cls.HEADERS,
            verify=False
        )
    
    @classmethod
    def update_route(cls, route_id, category_id=None, group_num=None, group_order=None):
        """Обновление маршрута"""
        # Собираем только те поля, которые нужно обновить
        data = {}
        if category_id is not None:
            data['category_id'] = category_id
        if group_num is not None:
            data['group_num'] = group_num
        if group_order is not None:
            data['group_order'] = group_order
            
        # Отправляем PUT запрос
        return requests.put(
            f"{cls.BASE_URL}/route/{route_id}",
            json=data,
            headers=cls.HEADERS,
            verify=False
        )
    
    @classmethod
    def get_routes(cls, page=1, limit=100, status_list=None, category_id_list=None, organization_id_list=None):
        """Получение списка маршрутов"""
        # Параметры запроса
        params = {
            'page': page,
            'limit': limit
        }
        
        # Добавляем фильтры, если они указаны
        if status_list:
            for status in status_list:
                params['status_list[]'] = status
        if category_id_list:
            for category_id in category_id_list:
                params['category_id_list[]'] = category_id
        if organization_id_list:
            for org_id in organization_id_list:
                params['organization_id_list[]'] = org_id
        
        # Отправляем GET запрос
        return requests.get(
            f"{cls.BASE_URL}/route/grouped",
            params=params,
            headers=cls.HEADERS,
            verify=False
        )
    
  
    
    @classmethod
    def delete_route(cls, route_id: int, headers: dict = None) -> requests.Response:
        """Удаление маршрута по ID"""
        # Используем стандартные заголовки, если не переданы свои
        req_headers = cls.HEADERS.copy()
        if headers:
            req_headers.update(headers)
        return requests.delete(
            f"{cls.BASE_URL}/route/{route_id}",
            headers=req_headers,
            verify=False
        )
    
    @classmethod
    def get_station(cls, station_id, headers=None):
        req_headers = cls.HEADERS.copy()
        if headers:
            req_headers.update(headers)
        return requests.get(f"{cls.BASE_URL}/station/{station_id}", headers=req_headers, verify=False)

    @classmethod
    def list_stations(cls, page=1, limit=10, headers=None):
        req_headers = cls.HEADERS.copy()
        if headers:
            req_headers.update(headers)
        params = {"page": page, "limit": limit}
        return requests.get(f"{cls.BASE_URL}/station", params=params, headers=req_headers, verify=False)

    @classmethod
    def create_station(cls, data, headers=None):
        req_headers = cls.HEADERS.copy()
        if headers:
            req_headers.update(headers)
        return requests.post(f"{cls.BASE_URL}/station", json=data, headers=req_headers, verify=False)

    @classmethod
    def update_station(cls, station_id, data, headers=None):
        req_headers = cls.HEADERS.copy()
        if headers:
            req_headers.update(headers)
        return requests.put(f"{cls.BASE_URL}/station/{station_id}", json=data, headers=req_headers, verify=False)

    @classmethod
    def delete_station(cls, station_id, headers=None):
        req_headers = cls.HEADERS.copy()
        if headers:
            req_headers.update(headers)
        return requests.delete(f"{cls.BASE_URL}/station/{station_id}", headers=req_headers, verify=False) 