from gettext import find

DEFAULT_PLANNER_PROMPT = """
你是一个顶级的AI规划专家。你的任务是将用户提出的复杂问题分解成一个由多个简单步骤组成的行动计划。
请确保计划中的每个步骤都是一个独立的、可执行的子任务，并且严格按照逻辑顺序排列。
你的输出必须是一个Python列表，其中每个元素都是一个描述子任务的字符串。

问题: {question}

请严格按照以下格式输出你的计划:
```python
["步骤1", "步骤2", "步骤3", ...]
```
"""

# 默认执行器提示词模板
DEFAULT_EXECUTOR_PROMPT = """
你是一位顶级的AI执行专家。你的任务是严格按照给定的计划，一步步地解决问题。
你将收到原始问题、完整的计划、以及到目前为止已经完成的步骤和结果。
请你专注于解决"当前步骤"，并仅输出该步骤的最终答案，不要输出任何额外的解释或对话。

# 原始问题:
{question}

# 完整计划:
{plan}

# 历史步骤与结果:
{history}

# 当前步骤:
{current_step}

请仅输出针对"当前步骤"的回答:
"""


from typing import Optional, List, Dict, Iterator
from hello_agents import PlanAndSolveAgent, HelloAgentsLLM, Config, Message
from hello_agents.agents.plan_solve_agent import Planner, Executor

class MyPlanAndSolveAgent(PlanAndSolveAgent):
    """
    重写PlanAndSolveAgent，以支持自定义提示词
    """
    def __init__(
            self,
            name,
            llm: HelloAgentsLLM,
            system_prompt: Optional[str] = None,
            config: Optional[Config] = None,
            custom_prompts: Optional[Dict[str, str]] = None
    ):
        super().__init__(self, name, llm, system_prompt, config)
        # 设置提示词模板：用户自定义优先，否则使用默认模板
        if custom_prompts:
            planner_prompt = custom_prompts.get("planner")
            excutor_prompt = custom_prompts.get("executor")
        else:
            planner_prompt = DEFAULT_PLANNER_PROMPT
            excutor_prompt = DEFAULT_EXECUTOR_PROMPT
        self.planner = Planner(llm, planner_prompt)
        self.executor = Executor(llm, excutor_prompt)

    def run(self, input_text: str, **kwargs) -> str:
        print(f"\n🤖 {self.name} 开始处理问题: {input_text}")

        # 1. 生成计划
        plan = self.planner.plan(input_text, **kwargs)
        if not plan:
            final_answer = "无法生成有效的行动计划，任务终止。"
            print(f"\n--- 任务终止 ---\n{final_answer}")
            self.add_message(Message(input_text, "user"))
            self.add_message(Message(final_answer, "answer"))
            return final_answer

        # 2. 执行计划
        final_answer = self.executor.execute(input_text, plan, **kwargs)
