import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict

# 从.env中加载环境变量
load_dotenv()

class SimpleLLMClient:
    """
    LLM客户端，用于调用兼容OpenAI接口的服务，并默认使用流式响应
    """
    def __init__(self, model: str = None, apiKey: str = None, baseUrl: str = None, timeout: int = None):
        self.modelId = model or os.getenv("MODEL_NAME")
        self.apiKey = apiKey or os.getenv("OPENAI_API_KEY")
        self.baseUrl = baseUrl or os.getenv("OPENAI_BASE_URL")
        self.timeout = timeout or int(os.getenv("LLM_TIMEOUT", 60))

        if not all([self.modelId, self.apiKey, self.baseUrl]):
            raise ValueError("模型ID、API密钥和服务地址必须被提供或在.env文件中定义。")

        self.client = OpenAI(api_key=apiKey, base_url=baseUrl, timeout=self.timeout)
    def think(self, messages: List[Dict[str, str]], temperature: float = 0.0) -> str:
        """
        调用大模型进行思考
        """
        print(f"🧠 正在调用 {self.modelId} 模型...")
        try:
            response = self.client.chat.completions.create(
                model=self.modelId,
                messages=messages,
                temperature=temperature,
                stream=True
            )

            print("✅ 大语言模型响应成功:")
            collected_content = []
            for chunk in response:
                content = chunk.choices[0].delta.content or ""
                print(content, end="", flush=True)
                collected_content.append(content)
            print()
            return "".join(collected_content)

        except Exception as e:
            print(f"❌ 调用LLM API时发生错误: {e}")
            return None

if __name__ == "__main__":
    try:
        llmClient = SimpleLLMClient()
        messages = [
            {"role": "system", "content": "You are a helpful assistant that writes Python code."},
            {"role": "user", "content": "写一个快速排序算法"}
        ]
        responseText = llmClient.think(messages)
        if responseText:
            print("\n\n--- 完整模型响应 ---")
            print(responseText)
        else:
            print("大模型响应结果为空！")

    except Exception as e:
        print(e)
