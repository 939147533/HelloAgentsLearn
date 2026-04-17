DEFAULT_PROMPTS = {
    "initial": """
请根据以下要求完成任务:

任务: {task}

请提供一个完整、准确的回答。
""",
    "reflect": """
请仔细审查以下回答，并找出可能的问题或改进空间:

# 原始任务:
{task}

# 当前回答:
{content}

请分析这个回答的质量，指出不足之处，并提出具体的改进建议。
如果回答已经很好，请回答"无需改进"。
""",
    "refine": """
请根据反馈意见改进你的回答:

# 原始任务:
{task}

# 上一轮回答:
{last_attempt}

# 反馈意见:
{feedback}

请提供一个改进后的回答。
"""
}

from typing import Optional, List, Dict, Iterator
from hello_agents import ReflectionAgent, HelloAgentsLLM, Config, Message, ToolRegistry

class MyReflectionAgent(ReflectionAgent):
    """
    重写ReflectionAgent
    """
    def __init__(
            self,
            name:str,
            llm: HelloAgentsLLM,
            system_prompt: Optional[str] = None,
            config: Optional[Config] = None,
            max_iterations: int = 5,
            custom_prompts: Optional[Dict[str, str]] = None
    ):
        super().__init__(name, llm, system_prompt, config) # 调用父类构造函数
        self.max_iterations = max_iterations
        self.current_history: List[str] = []
        self.prompt_templates = custom_prompts if custom_prompts else DEFAULT_PROMPTS
        print(f"✅ {name} 初始化完成，最大步数: {max_iterations}")

    def run(self, input_text: str, **kwargs) -> str:
        """运行Reflection Agent"""
        print(f"\n🤖 {self.name} 开始处理问题: {input_text}")

        # 1. 初始执行
        print("\n--- 正在进行初始尝试 ---")
        initial_prompt = self.prompt_templates["initial"].format(
            task = input_text
        )
        init_response = self._get_llm_response(initial_prompt, **kwargs)
        print(f"\n初始响应: {init_response}")
        self.memory.add_record("execution", init_response)
        # 2. 迭代循环：反思与优化
        for i in range(self.max_iterations):
            print(f"\n--- 第 {i+1}/{self.max_iterations} 轮迭代 ---")

            # a. 反思
            print("\n-> 正在进行反思...")
            last_result = self.memory.get_last_execution()
            reflect_prompt = self.prompt_templates["reflect"].format(
                task = input_text,
                content = last_result
            )
            messages = [{"role": "user", "content": reflect_prompt}]
            # 流式调用LLM
            reflect_response = ""
            print("📝 实时响应: ", end="")
            for chunk in self.llm.stream_invoke(messages, **kwargs):
                reflect_response += chunk
            # reflect_resp  onse = self._get_llm_response(reflect_prompt, **kwargs)
            self.memory.add_record("reflection", reflect_response)

            # b. 检查是否需要停止
            if "无需改进" in reflect_response or "no need for improvement" in reflect_response:
                print("\n✅ 反思认为结果已无需改进，任务完成。")
                break

            # c. 优化
            print("\n-> 正在进行优化...")
            refine_prompt = self.prompt_templates["refine"].format(
                task = input_text,
                last_attempt = last_result,
                feedback = reflect_response
            )
            messages = [{"role": "user", "content": refine_prompt}]
            print("📝 实时响应: ", end="")
            refine_response = ""
            for chunk in self.llm.stream_invoke(messages, **kwargs):
                refine_response += chunk
            # refine_response = self._get_llm_response(refine_prompt, **kwargs)
            self.memory.add_record("execution", refine_response)

        final_result = self.memory.get_last_execution()
        print(f"\n--- 任务完成 ---\n最终结果:\n{final_result}")

        # 保存到历史记录
        self.add_message(Message(input_text, "user"))
        self.add_message(Message(final_result, "assistant"))

        return final_result

