import requests

class APIClient():
    def __init__(self,url):
        self.url = url
    def get_products(self,timeout=5):
        try:
            response = requests.get(self.url,timeout=timeout)
            response.raise_for_status()
        except requests.RequestException:
            print("请求失败")
            return None
        else:
            return response.json()

