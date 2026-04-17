import requests
import os

# 建议将 API Key 存储在环境变量中，不要硬编码
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city: str):
    """
    获取指定城市的当前天气
    :param city: 城市名称（建议英文，如 Beijing, London）
    """
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric',  # metric=摄氏度, imperial=华氏度
        'lang': 'zh_cn'  # 返回中文描述
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()  # 检查 HTTP 错误
        return response.json()
    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
            print(f"未找到城市: {city}")
        elif response.status_code == 401:
            print("API Key 无效或尚未激活，请检查配置")
        else:
            print(f"HTTP 错误: {err}")
    except requests.exceptions.Timeout:
        print("请求超时，请检查网络连接")
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
    return None


def display_weather(data):
    """格式化输出天气信息"""
    if not data:
        return

    city = data.get('name', '未知')
    main = data.get('main', {})
    weather = data.get('weather', [{}])[0]
    wind = data.get('wind', {})

    print(f"\n🌍 {city} 当前天气")
    print(f"🌡️ 温度: {main.get('temp')}°C (体感 {main.get('feels_like')}°C)")
    print(f"💧 湿度: {main.get('humidity')}%")
    print(f"🌤️ 天气: {weather.get('description')}")
    print(f"💨 风速: {wind.get('speed')} m/s")
    print(f"🔽 气压: {main.get('pressure')} hPa")


# 使用示例
if __name__ == "__main__":
    city = input("请输入城市名称（英文）: ") or "Beijing"
    weather_data = get_weather(city)
    display_weather(weather_data)