import requests


class HttpMethods:
    headers = {
        "Accept":"application/json, text/plain, */*",
        "Accept-Language":"en-US,en;q=0.9,ru;q=0.8",
        "Authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiMDI2M2Q4N2YyMDJhNzRmMTlkYzkxZmY2ZjRmMTdlMjcwYTFhZDFkMDhhNGFlYzkyMmFmNTkyMmVlYTAyOGJlMGFkM2UzNzBhYjUyZGUzZWUiLCJpYXQiOjE3NDMxNTMxNzguMjI5MTIyLCJuYmYiOjE3NDMxNTMxNzguMjI5MTI1LCJleHAiOjE3NDQ0NDkxNzcuOTE1MjY4LCJzdWIiOiI1MCIsInNjb3BlcyI6W10sIm9yZ2FuaXphdGlvbl9pZF9saXN0IjpbXSwiaWRlbnRpZmllciI6ImEudmVzZWxvdl9BQUFfZm9ybWF0dHdvLnJ1XzE2NDE4MTk4ODMuNDA4OSIsImVtYWlsIjoiYS52ZXNlbG92QGZvcm1hdHR3by5ydSIsInVzZXJfbmFtZSI6ImEudmVzZWxvdkBmb3JtYXR0d28ucnUiLCJmaXJzdF9uYW1lIjoi0JDQu9C10LrRgdCw0L3QtNGAIiwibGFzdF9uYW1lIjoi0JLQtdGB0LXQu9C-0LIiLCJtaWRkbGVfbmFtZSI6ItCS0LjQutGC0L7RgNC-0LLQuNGHIn0.nQkyvAX1VdYZl8OKJ1ZiCaR1j515eXRYfDOVJU78MvlqMuQ-kzz6rP6v7ImVexgMMMUwECXE21j0fmO9-fJ1Hm5xu5PDZutjV_6mvR1vuPUvf5AzeaflZACxbRB9SjYmVp2Jz7jjGpSP7Ud1TYjYSxOrr21fxulqBYsylMi2Y4ePZbupodDTP5FgyULV5eNDHlcRdQkj1QYgl35ag9lVcmULhSffC9vkvXPcaAe7YabAr8TllbfeiCJ4f6QaRZZ1W7PH3gDCIg3pP2xCV1aPfMY613mb9FRGBESBxl1OMQHyUmQgHHWS3n-uxRBgZOjh0les28qlXR7O5CyZtAZxGe2FiICsclgwmx7IB5FGQUkWHJ2EqveIyuLvH-LEFrIAhkxP1uIq9mJrjuWnLGfvHH3wvKUXXu-WGSrBQq0xny0vG_SrE56Byg4hLtKXyRN5F2ey0tR4B3H7gyNdCS_J_-x7wb2qMGZG0KGbB2iqy4sz3eIa0su7Ff_agBBHREky5koy-v_Gux_C9sItlBpwLANqLnJu9qBr9EnVnCUFM29Je6unaszIAcgi6LAMO3pyQYqW3_KzDvRuGfVepYNUoMug-IAwcrXQ95s5gnZMvMDGy2vTHykjuKxy_VrxrYchVlKBtWXgJHKNifXAjmi9ZvOwZgi2g_L3uhz5EX3eAzs",
        "Cache-Control":"no-cache",
        "Connection":"keep-alive",
        "Pragma":"no-cache",
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "project":"46_krs",
        "service":"eputs"
    }
    cookies = {}

    @staticmethod
    def get(url):
        """GET request"""
        response = requests.get(url, headers=HttpMethods.headers, cookies=HttpMethods.cookies)
        return response

    @staticmethod
    def post(url, body):
        """POST request"""
        response = requests.post(url, json=body, headers=HttpMethods.headers, cookies=HttpMethods.cookies)
        return response

    @staticmethod
    def put(url, body):
        """PUT request"""
        response = requests.put(url, json=body, headers=HttpMethods.headers, cookies=HttpMethods.cookies)
        return response

    @staticmethod
    def delete(url):
        """DELETE request"""
        response = requests.delete(url, headers=HttpMethods.headers, cookies=HttpMethods.cookies)
        return response

