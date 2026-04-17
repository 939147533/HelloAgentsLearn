from typing import Dict, Any
from SerpApiClient import search
from dotenv import load_dotenv

class ToolExecutor:
    """
    工具执行器，负责管理和执行工具
    """
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}

    def registerTool(self, name: str, description: str, func: callable):
        """
        向工具箱中注册新工具
        """
        if name in self.tools:
            print(f"警告：工具 '{name}' 已存在， 将覆盖原有工具。")
        self.tools[name] = {"description": description, "func": func}
        print(f"工具 '{name}' 注册成功。")

    def getTools(self, name: str) -> callable:
        """
        根据名称获取工具的执行函数
        """
        return self.tools.get(name).get("func")

    def getAvailableTools(self) -> str:
        """
        获取所有可用工具的描述
        """
        return "\n".join([
            f"- {name}: {info['description']}"
            for name, info in self.tools.items()
        ])

if __name__ == "__main__":
    # 从.env中加载环境变量
    load_dotenv()
    # 初始化工具执行器
    toolExecutor = ToolExecutor()

    # 注册工具
    search_description = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
    toolExecutor.registerTool("Search", search_description, search)

    print("\n--- 可用的工具 ---")
    print(toolExecutor.getAvailableTools())

    # 4. 智能体的Action调用
    print("\n--- 执行 Action: Search['英伟达最新的GPU型号是什么'] ---")
    tool_name = "Search"
    tool_input = "英伟达最新的GPU型号是什么"
    tool_function = toolExecutor.getTools(tool_name)
    if tool_function:
        observation = tool_function(tool_input)
        print("--- 观察 (Observation) ---")
        print(observation)
    else:
        print(f"错误:未找到名为 '{tool_name}' 的工具。")
