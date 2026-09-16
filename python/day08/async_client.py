import asyncio
import httpx

class AsyncAPIClient():
    def __init__(self,base_url,timeout):
        self.base_url = base_url
        self.timeout = timeout
    async def get(self,path):
        url = self.base_url + path
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url=url,timeout=self.timeout)
                response.raise_for_status()
                content_type = response.headers.get("content-type", "")
                if "application/json" in content_type: 
                    return {"code_status":"success","data":response.json()}
                else:
                    return {"code_status":"success","data":response.text}
        except httpx.TimeoutException as e:
            print("请求超时")
            return  {"code_status":"failed","url":url,"reason":str(e)}
        except httpx.HTTPStatusError as e:
            print("HTTP 请求失败")
            return  {"code_status":"failed","url":url,"reason":str(e)}
        except httpx.RequestError as e:
            print("请求失败")
            return  {"code_status":"failed","url":url,"reason":str(e)}

    async def post(self,path,data):
        url = self.base_url + path
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url=url,
                    json=data,
                    timeout=self.timeout
                    )
                response.raise_for_status()
                content_type = response.headers.get("content-type", "")
                if "application/json" in content_type: 
                    return {"code_status":"success","data":response.json()}
                else:
                    return {"code_status":"success","data":response.text}
        except httpx.TimeoutException as e:
            print("请求超时")
            return  {"code_status":"failed","url":url,"reason":str(e)}
        except httpx.HTTPStatusError as e:
            print("HTTP 请求失败")
            return  {"code_status":"failed","url":url,"reason":str(e)}
        except httpx.RequestError as e:
            print("请求失败")
            return  {"code_status":"failed","url":url,"reason":str(e)}