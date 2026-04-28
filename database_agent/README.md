# 数据库Agent助手

基于hello-agents库实现的智能数据库查询助手，支持将自然语言转换为SQL查询并从Oracle数据库获取数据。

## 功能特性

- 🤖 **自然语言查询**: 用中文描述查询需求，自动转换为SQL语句
- 🗄️ **Oracle数据库支持**: 完整支持Oracle数据库连接和查询
- 📊 **表格化输出**: 查询结果以美观的表格形式展示
- 🔒 **安全验证**: SQL语句自动验证，防止危险操作
- 🎯 **智能推理**: 基于ReAct框架的智能推理和工具调用

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置说明

1. 复制示例配置文件:
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，配置以下参数:

### LLM配置
- `LLM_MODEL_ID`: 模型ID，如 `Qwen/Qwen2.5-7B-Instruct`
- `LLM_API_KEY`: API密钥
- `LLM_BASE_URL`: API服务地址

### Oracle数据库配置
- `DB_HOST`: 数据库主机地址
- `DB_PORT`: 数据库端口 (默认: 1521)
- `DB_SERVICE_NAME`: 服务名称
- `DB_USERNAME`: 用户名
- `DB_PASSWORD`: 密码

## 使用方法

### 基本使用

```python
from database_agent import DatabaseAgent, DatabaseConfig
from hello_agents import HelloAgentsLLM
import os

# 初始化LLM
llm = HelloAgentsLLM(
    model=os.getenv("LLM_MODEL_ID"),
    apiKey=os.getenv("LLM_API_KEY"),
    baseUrl=os.getenv("LLM_BASE_URL")
)

# 配置数据库
db_config = DatabaseConfig(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    service_name=os.getenv("DB_SERVICE_NAME"),
    username=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD")
)

# 创建Agent
agent = DatabaseAgent(
    name="DatabaseAssistant",
    llm=llm,
    db_config=db_config,
    max_steps=5
)

# 执行查询
result = agent.run("查询所有员工信息")
print(result)
```

### 交互式使用

运行主程序进入交互模式:

```bash
python main.py
```

## 查询示例

- "查询所有员工信息"
- "查询工资大于5000的员工"
- "统计各部门的员工数量"
- "查询最近入职的5名员工"
- "查询IT部门的员工平均工资"

## 项目结构

```
database_agent/
├── __init__.py          # 包初始化
├── agent.py             # DatabaseAgent主类
├── config.py            # 数据库配置管理
├── tools.py             # 工具集 (OracleQueryTool, SQLGeneratorTool)
├── main.py              # 主程序
├── requirements.txt     # 依赖列表
├── .env.example        # 配置示例
└── README.md           # 说明文档
```

## 技术架构

基于HelloAgentsLearn项目中的ReAct框架实现:

- **ReAct Agent**: 推理-行动循环框架
- **Tool Registry**: 工具注册和管理
- **LLM Integration**: 大语言模型集成
- **Oracle DB**: Oracle数据库连接和查询

## 可用工具

1. **GetSchema**: 获取数据库表结构信息
2. **GenerateSQL**: 将自然语言转换为SQL语句
3. **ExecuteQuery**: 执行SQL查询并返回结果

## 安全特性

- SQL语句自动验证，防止危险操作
- 只允许SELECT查询，禁止修改操作
- 参数化查询，防止SQL注入

## 注意事项

1. 确保Oracle数据库已正确配置并可访问
2. 确保LLM API密钥有效且有足够配额
3. 首次使用时会获取数据库表结构，请确保有相应权限
4. 复杂查询可能需要多次推理步骤

## 许可证

MIT License