# 数据库Agent助手 - 使用指南

## 快速开始

### 1. 安装依赖

```bash
cd database_agent
pip install -r requirements.txt
```

### 2. 配置环境变量

复制示例配置文件并编辑:

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入实际的配置信息:

```env
# LLM配置
LLM_MODEL_ID=Qwen/Qwen2.5-7B-Instruct
LLM_API_KEY=your_actual_api_key
LLM_BASE_URL=https://api.modelscope.cn/v1

# Oracle数据库配置
DB_HOST=localhost
DB_PORT=1521
DB_SERVICE_NAME=ORCL
DB_USERNAME=system
DB_PASSWORD=your_actual_password
```

### 3. 创建测试数据库

使用提供的SQL脚本创建测试表和数据:

```bash
# 在Oracle SQL*Plus或其他Oracle客户端中执行
sqlplus system/password@localhost:1521/ORCL @setup_database.sql
```

### 4. 运行测试

```bash
# 运行测试套件
python test.py

# 运行演示程序
python demo.py

# 运行交互式演示
python demo.py interactive

# 运行主程序
python main.py
```

## 详细使用说明

### 基本查询示例

```python
from database_agent import DatabaseAgent, DatabaseConfig
from hello_agents import HelloAgentsLLM
import os

# 初始化
llm = HelloAgentsLLM(
    model=os.getenv("LLM_MODEL_ID"),
    apiKey=os.getenv("LLM_API_KEY"),
    baseUrl=os.getenv("LLM_BASE_URL")
)

db_config = DatabaseConfig()
agent = DatabaseAgent(
    name="MyAssistant",
    llm=llm,
    db_config=db_config
)

# 执行查询
result = agent.run("查询所有员工信息")
print(result)
```

### 支持的查询类型

1. **简单查询**
   - "查询所有员工信息"
   - "查询所有部门"

2. **条件查询**
   - "查询工资大于5000的员工"
   - "查询IT部门的员工"
   - "查询2020年以后入职的员工"

3. **统计查询**
   - "统计各部门的员工数量"
   - "计算全公司的平均工资"
   - "统计每个部门的总工资"

4. **排序和限制**
   - "查询工资最高的前5名员工"
   - "查询最近入职的3名员工"

5. **聚合查询**
   - "查询各部门的平均工资"
   - "统计每个部门的项目数量"

### 工作原理

1. **用户输入自然语言查询**
2. **Agent分析查询需求**
3. **调用GetSchema获取数据库结构**
4. **调用GenerateSQL生成SQL语句**
5. **调用ExecuteQuery执行查询**
6. **格式化并返回结果**

### 自定义配置

#### 修改最大推理步数

```python
agent = DatabaseAgent(
    name="MyAssistant",
    llm=llm,
    db_config=db_config,
    max_steps=10  # 增加最大步数
)
```

#### 使用不同的LLM

```python
llm = HelloAgentsLLM(
    model="gpt-4",
    apiKey="your_openai_key",
    baseUrl="https://api.openai.com/v1"
)
```

#### 连接到不同的数据库

```python
db_config = DatabaseConfig(
    host="192.168.1.100",
    port=1521,
    service_name="PRODDB",
    username="app_user",
    password="secure_password"
)
```

## 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查Oracle数据库是否运行
   - 验证连接参数是否正确
   - 确认网络连接正常

2. **LLM API调用失败**
   - 检查API密钥是否有效
   - 确认API服务地址正确
   - 检查网络连接和防火墙设置

3. **SQL生成不准确**
   - 确保数据库表结构正确
   - 尝试更明确的自然语言描述
   - 考虑增加max_steps参数

4. **查询结果为空**
   - 检查数据库中是否有数据
   - 验证生成的SQL语句是否正确
   - 确认查询条件是否合适

### 调试技巧

1. **启用详细日志**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

2. **检查生成的SQL**
```python
# 在tools.py中添加调试输出
print(f"生成的SQL: {sql}")
```

3. **测试数据库连接**
```python
from database_agent import OracleQueryTool, DatabaseConfig

config = DatabaseConfig()
tool = OracleQueryTool(config)
if tool.connect():
    print("连接成功")
    tool.disconnect()
```

## 性能优化

1. **缓存表结构**
   - Agent会自动缓存数据库表结构
   - 避免重复获取schema信息

2. **批量查询**
   - 将多个相关查询合并为一个
   - 使用JOIN代替多次查询

3. **索引优化**
   - 为常用查询字段创建索引
   - 定期分析表统计信息

## 安全建议

1. **保护敏感信息**
   - 不要将.env文件提交到版本控制
   - 使用环境变量存储密码
   - 定期更换API密钥

2. **限制查询权限**
   - 使用只读数据库用户
   - 限制可访问的表和字段
   - 设置查询超时时间

3. **SQL注入防护**
   - 使用参数化查询
   - 验证生成的SQL语句
   - 禁止危险操作

## 扩展功能

### 添加新的工具

```python
from database_agent import DatabaseAgent

class CustomAgent(DatabaseAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 注册自定义工具
        self.tool_registry.register_tool(
            "CustomTool",
            "自定义工具描述",
            self._custom_tool_function
        )
    
    def _custom_tool_function(self, input_text: str) -> str:
        # 实现自定义逻辑
        return "自定义结果"
```

### 支持其他数据库

修改 `tools.py` 中的 `OracleQueryTool` 类，适配其他数据库:

```python
import psycopg2  # PostgreSQL
# 或
import pymysql   # MySQL
```

## 最佳实践

1. **查询设计**
   - 使用清晰明确的自然语言
   - 避免歧义的表达
   - 提供足够的上下文信息

2. **数据库设计**
   - 使用有意义的表名和字段名
   - 添加适当的注释
   - 维护良好的文档

3. **错误处理**
   - 捕获并处理异常
   - 提供友好的错误信息
   - 记录详细的日志

## 示例场景

### 场景1: 人力资源查询

```python
# 查询员工信息
agent.run("查询IT部门的所有员工")

# 统计部门人数
agent.run("统计每个部门的员工数量")

# 查询薪资信息
agent.run("查询工资最高的10名员工")
```

### 场景2: 财务分析

```python
# 部门预算分析
agent.run("查询各部门的预算和实际支出")

# 成本统计
agent.run("统计IT部门的人力成本")

# 项目财务
agent.run("查询所有项目的预算和状态")
```

### 场景3: 项目管理

```python
# 项目进度
agent.run("查询所有进行中的项目")

# 项目统计
agent.run("统计每个部门的项目数量")

# 资源分配
agent.run("查询参与项目最多的员工")
```

## 技术支持

如有问题，请检查:
1. README.md - 基本说明
2. setup_database.sql - 数据库结构
3. test.py - 测试用例
4. demo.py - 使用示例

## 更新日志

### v1.0.0 (2024-01-01)
- 初始版本发布
- 支持基本的自然语言查询
- Oracle数据库集成
- 表格化结果输出