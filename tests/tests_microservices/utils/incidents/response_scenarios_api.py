import requests
from config.config import BASE_URL, HEADERS

class ResponseScenariosAPI:
    """API для работы со сценариями реагирования"""

    # Базовый URL для сценариев реагирования
    BASE_SCENARIOS_URL = "http://91.227.17.139/services/react/api/response-scenario"

    # Заголовки по умолчанию с новым токеном
    HEADERS = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiMDkxYTNlNzI2ODQ5YzE2ZDZiNTdmOGE3YjRlZTA0ZDNlZTNhNDBkNzgxMmYxNjA0NDc0YjhkOTEzNGJmODkzYTkwYzVjZTRmMDIxOTIyMjYiLCJpYXQiOjE3NTM3OTU5NzYuMzM0MjkzLCJuYmYiOjE3NTM3OTU5NzYuMzM0MzA1LCJleHAiOjE3NTUwOTE5NzYuMTM1MzM4LCJzdWIiOiI2OCIsInNjb3BlcyI6W10sIm9yZ2FuaXphdGlvbl9pZF9saXN0IjpbXSwiaWRlbnRpZmllciI6ImEudmVzZWxvdjFfQUFBX2Zvcm1hdHR3by5ydV8xNzQ4NTQ2MjU2Ljg4MzciLCJlbWFpbCI6ImEudmVzZWxvdjFAZm9ybWF0dHdvLnJ1IiwidXNlcl9uYW1lIjoiYS52ZXNlbG92MUBmb3JtYXR0d28ucnUiLCJmaXJzdF9uYW1lIjoi0JDQu9C10LrRgdCw0L3QtNGAIiwibGFzdF9uYW1lIjoi0JLQtdGB0LXQu9C-0LIiLCJtaWRkbGVfbmFtZSI6ItCS0LjQutGC0L7RgNC-0LLQuNGHIn0.EVf1vqr3cbqYvwdXI741_aM7xFtda1xagsVnUMKtxGC8wN3AzK4CQmRMmcEWxNF0Mh7Hsft-BRVc7Kx47rnSQW-MRjY9_D3QxdxsNhzurvW9SysP40yAG8WnIWAdynVOzGxLE8DVtFKo1Dhl29UKKUeCnB0zznRycMVwj9SoedegRqq5jFRpxWnVusECpvbpMCUIPe5YsAbUp0QC8KDqeAumCGYSBsHBRxvuPgwgq0RQX4WK0o8NaH73X7ZhBiOiue899YMn9maOMBwFk-1Tn0bzyswlzET2lTAvpaEXk2Ou7mrDKcWosbFDF-vWidqLInRKBRX7AQbBeRUqC6Fc2eLQCctOjSfWtW5EpZ5M2c9VP6RoYSjq1ywW2D0nsIWTN58ciEoPELwMK6Bq53bw6xckJrh0NDprFerRLt86h0qMUTOfJOpTiHfFSlrJ8wmgaKrVdHhEVmI23OYzV1wpMip1NRyRp1fvBDbNwJGnVINO87yui7ZmBtn7gIo59yhhC0NQfNTjgobvfOTssKf8Ed1swRRaZdQ7GJ_ce_1rx4seBL1l2KXn-QKGIAANQ4906llNRvLfYiY9NiUQBoi7BfHqQWWRqJT024i2DjbxYv0qprJjhWn4u34VVLY9ov45D4gS6rRgOBivkyXofz1Ys4lTOQoplhH6fhRnc2bCNGs",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "http://91.227.17.139",
        "Referer": "http://91.227.17.139/react/dictionaries/response-scenarios?limit=25&page=1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
        "project": "98_spb",
        "service": "eputs"
    }

    @classmethod
    def create_scenario(cls, data, headers=None):
        """Создание нового сценария реагирования"""
        if headers is None:
            headers = cls.HEADERS

        url = cls.BASE_SCENARIOS_URL
        response = requests.post(url, json=data, headers=headers, timeout=10)
        return response

    @classmethod
    def get_scenarios_list(cls, params=None, headers=None):
        """Получение списка сценариев реагирования"""
        if headers is None:
            headers = cls.HEADERS
            
        url = cls.BASE_SCENARIOS_URL
        response = requests.get(url, params=params, headers=headers, timeout=30)  # Увеличиваем таймаут
        return response

    @classmethod
    def get_scenario_by_id(cls, scenario_id, headers=None):
        """Получение сценария по ID"""
        if headers is None:
            headers = cls.HEADERS

        url = f"{cls.BASE_SCENARIOS_URL}/{scenario_id}"
        response = requests.get(url, headers=headers, timeout=10)
        return response

    @classmethod
    def update_scenario(cls, scenario_id, data, headers=None):
        """Обновление сценария реагирования"""
        if headers is None:
            headers = cls.HEADERS

        url = f"{cls.BASE_SCENARIOS_URL}/{scenario_id}"
        response = requests.put(url, json=data, headers=headers, timeout=10)
        return response

    @classmethod
    def delete_scenario(cls, scenario_id, headers=None):
        """Удаление сценария реагирования"""
        if headers is None:
            headers = cls.HEADERS

        url = f"{cls.BASE_SCENARIOS_URL}/{scenario_id}"
        response = requests.delete(url, headers=headers, timeout=10)
        return response 