import requests
from typing import Dict, Any, Optional, List
from datetime import datetime

class EventsAPI:
    """API для работы с мероприятиями (events)"""
    
    # Базовый URL API
    BASE_URL = "http://91.227.17.139/services/react/api"
    
    # Общие заголовки для всех запросов
    HEADERS = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiMDkxYTNlNzI2ODQ5YzE2ZDZiNTdmOGE3YjRlZTA0ZDNlZTNhNDBkNzgxMmYxNjA0NDc0YjhkOTEzNGJmODkzYTkwYzVjZTRmMDIxOTIyMjYiLCJpYXQiOjE3NTM3OTU5NzYuMzM0MjkzLCJuYmYiOjE3NTM3OTU5NzYuMzM0MzA1LCJleHAiOjE3NTUwOTE5NzYuMTM1MzM4LCJzdWIiOiI2OCIsInNjb3BlcyI6W10sIm9yZ2FuaXphdGlvbl9pZF9saXN0IjpbXSwiaWRlbnRpZmllciI6ImEudmVzZWxvdjFfQUFBX2Zvcm1hdHR3by5ydV8xNzQ4NTQ2MjU2Ljg4MzciLCJlbWFpbCI6ImEudmVzZWxvdjFAZm9ybWF0dHdvLnJ1IiwidXNlcl9uYW1lIjoiYS52ZXNlbG92MUBmb3JtYXR0d28ucnUiLCJmaXJzdF9uYW1lIjoi0JDQu9C10LrRgdCw0L3QtNGAIiwibGFzdF9uYW1lIjoi0JLQtdGB0LXQu9C-0LIiLCJtaWRkbGVfbmFtZSI6ItCS0LjQutGC0L7RgNC-0LLQuNGHIn0.EVf1vqr3cbqYvwdXI741_aM7xFtda1xagsVnUMKtxGC8wN3AzK4CQmRMmcEWxNF0Mh7Hsft-BRVc7Kx47rnSQW-MRjY9_D3QxdxsNhzurvW9SysP40yAG8WnIWAdynVOzGxLE8DVtFKo1Dhl29UKKUeCnB0zznRycMVwj9SoedegRqq5jFRpxWnVusECpvbpMCUIPe5YsAbUp0QC8KDqeAumCGYSBsHBRxvuPgwgq0RQX4WK0o8NaH73X7ZhBiOiue899YMn9maOMBwFk-1Tn0bzyswlzET2lTAvpaEXk2Ou7mrDKcWosbFDF-vWidqLInRKBRX7AQbBeRUqC6Fc2eLQCctOjSfWtW5EpZ5M2c9VP6RoYSjq1ywW2D0nsIWTN58ciEoPELwMK6Bq53bw6xckJrh0NDprFerRLt86h0qMUTOfJOpTiHfFSlrJ8wmgaKrVdHhEVmI23OYzV1wpMip1NRyRp1fvBDbNwJGnVINO87yui7ZmBtn7gIo59yhhC0NQfNTjgobvfOTssKf8Ed1swRRaZdQ7GJ_ce_1rx4seBL1l2KXn-QKGIAANQ4906llNRvLfYiY9NiUQBoi7BfHqQWWRqJT024i2DjbxYv0qprJjhWn4u34VVLY9ov45D4gS6rRgOBivkyXofz1Ys4lTOQoplhH6fhRnc2bCNGs",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "http://91.227.17.139",
        "Referer": "http://91.227.17.139/react/dictionaries/events",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
        "project": "98_spb",
        "service": "eputs"
    }
    
    @classmethod
    def create_event(cls, data: Dict[str, Any], headers: Dict[str, str] = None) -> requests.Response:
        """Создание нового мероприятия"""
        req_headers = cls.HEADERS.copy()
        if headers:
            req_headers.update(headers)
        return requests.post(
            f"{cls.BASE_URL}/event/",
            json=data,
            headers=req_headers,
            verify=False
        )
    
    @classmethod
    def get_event(cls, event_id: int, headers: Dict[str, str] = None) -> requests.Response:
        """Получение мероприятия по ID"""
        req_headers = cls.HEADERS.copy()
        if headers:
            req_headers.update(headers)
        return requests.get(
            f"{cls.BASE_URL}/event/{event_id}",
            headers=req_headers,
            verify=False
        )
    
    @classmethod
    def update_event(cls, event_id: int, data: Dict[str, Any], headers: Dict[str, str] = None) -> requests.Response:
        """Обновление мероприятия"""
        req_headers = cls.HEADERS.copy()
        if headers:
            req_headers.update(headers)
        return requests.put(
            f"{cls.BASE_URL}/event/{event_id}",
            json=data,
            headers=req_headers,
            verify=False
        )
    
    @classmethod
    def delete_event(cls, event_id: int, headers: Dict[str, str] = None) -> requests.Response:
        """Удаление мероприятия"""
        req_headers = cls.HEADERS.copy()
        if headers:
            req_headers.update(headers)
        return requests.delete(
            f"{cls.BASE_URL}/event/{event_id}",
            headers=req_headers,
            verify=False
        )
    
    @classmethod
    def list_events(cls, page: int = 1, limit: int = 25, headers: Dict[str, str] = None) -> requests.Response:
        """Получение списка мероприятий"""
        req_headers = cls.HEADERS.copy()
        if headers:
            req_headers.update(headers)
        params = {"page": page, "limit": limit}
        return requests.get(
            f"{cls.BASE_URL}/event/",
            params=params,
            headers=req_headers,
            verify=False
        )
    
    @classmethod
    def get_event_routes(cls, headers: Dict[str, str] = None) -> requests.Response:
        """Получение списка маршрутов мероприятий"""
        req_headers = cls.HEADERS.copy()
        if headers:
            req_headers.update(headers)
        return requests.get(
            f"{cls.BASE_URL}/event/route",
            headers=req_headers,
            verify=False
        )
    
    @classmethod
    def get_routes_in_polygon(cls, polygon_data: Dict[str, Any], headers: Dict[str, str] = None) -> requests.Response:
        """Получение маршрутов мероприятий в полигоне"""
        req_headers = cls.HEADERS.copy()
        if headers:
            req_headers.update(headers)
        return requests.post(
            f"{cls.BASE_URL}/event/route-in-polygon",
            json=polygon_data,
            headers=req_headers,
            verify=False
        )
    
    @classmethod
    def get_event_object_types(cls, headers: Dict[str, str] = None) -> requests.Response:
        """Получение списка типов объектов мероприятий"""
        req_headers = cls.HEADERS.copy()
        if headers:
            req_headers.update(headers)
        return requests.get(
            f"{cls.BASE_URL}/event-object/type/",
            headers=req_headers,
            verify=False
        ) 