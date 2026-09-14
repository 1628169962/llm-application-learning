import requests
class APIClient:
    def __init__(self,base_url):
        self.base_url = base_url

    def get(self, path,headers=None,timeout=5):
        url = self.base_url + path
        try:
            response = requests.get(url,headers=headers,timeout=timeout)
            response.raise_for_status()
            return response
        except requests.HTTPError:
            print("HTTP 请求错误")
        except requests.Timeout:
            print("请求超时")
        except requests.ConnectionError:
            print("连接失败")
        except requests.RequestException:
            print("请求失败")
    def post(self,path,json=None,headers=None,timeout=5):
        url = self.base_url + path
        try:
            response = requests.post(url,json=json,headers=headers,timeout=timeout)
            response.raise_for_status()
            return response
        except requests.HTTPError:
            print("HTTP 请求错误")
        except requests.Timeout:
            print("请求超时")
        except requests.ConnectionError:
            print("连接失败")
        except requests.RequestException:
            print("请求失败")

