# 测试天气 API
import requests
# response = requests.get("https://wttr.in/Beijing?format=j1")
# print("天气API状态:", response.status_code)

# try:
#     response = requests.get("http://ip-api.com/json/", timeout=5)
#     data = response.json()
#     print(f"当前城市: {data.get('city')}")
#     print(f"天气信息请使用其他 API 获取")
# except Exception as e:
#     print(f"获取位置信息失败: {e}")


# 测试 Tavily API
from tavily import TavilyClient
tavily = TavilyClient(api_key="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")
try:
    result = tavily.search("test", search_depth="basic")
    print("Tavily API 连接成功")
except Exception as e:
    print("Tavily API 错误:", e)

