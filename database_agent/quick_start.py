"""
数据库Agent助手 - 快速开始示例
最简单的使用示例，帮助用户快速上手
"""

import os
from dotenv import load_dotenv

load_dotenv()

def quick_start():
    """快速开始示例"""
    
    print("=" * 70)
    print("🚀 数据库Agent助手 - 快速开始")
    print("=" * 70)
    
    print("\n📋 前置条件检查:")
    
    # 检查环境变量
    required_vars = ['LLM_MODEL_ID', 'LLM_API_KEY', 'LLM_BASE_URL',
                     'DB_HOST', 'DB_PORT', 'DB_SERVICE_NAME', 
                     'DB_USERNAME', 'DB_PASSWORD']
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ 缺少以下环境变量:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 解决方案:")
        print("   1. 复制 .env.example 为 .env")
        print("   2. 编辑 .env 文件，填入实际的配置信息")
        return False
    
    print("✅ 所有必需的环境变量已配置")
    
    # 检查依赖
    print("\n📦 检查Python依赖...")
    try:
        import oracledb
        print("✅ oracledb 已安装")
    except ImportError:
        print("❌ oracledb 未安装")
        print("   运行: pip install oracledb")
        return False
    
    try:
        import hello_agents
        print("✅ hello-agents 已安装")
    except ImportError:
        print("❌ hello-agents 未安装")
        print("   运行: pip install hello-agents")
        return False
    
    print("\n" + "=" * 70)
    print("🎯 快速开始代码示例")
    print("=" * 70)
    
    code_example = '''
# 1. 导入必要的模块
from database_agent import DatabaseAgent, DatabaseConfig
from hello_agents import HelloAgentsLLM
import os

# 2. 初始化LLM
llm = HelloAgentsLLM(
    model=os.getenv("LLM_MODEL_ID"),
    apiKey=os.getenv("LLM_API_KEY"),
    baseUrl=os.getenv("LLM_BASE_URL")
)

# 3. 配置数据库
db_config = DatabaseConfig(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    service_name=os.getenv("DB_SERVICE_NAME"),
    username=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD")
)

# 4. 创建Agent
agent = DatabaseAgent(
    name="MyDatabaseAssistant",
    llm=llm,
    db_config=db_config,
    max_steps=5
)

# 5. 执行查询
result = agent.run("查询所有员工信息")
print(result)
'''
    
    print(code_example)
    
    print("\n" + "=" * 70)
    print("💡 常用查询示例")
    print("=" * 70)
    
    examples = [
        "查询所有员工信息",
        "查询工资大于5000的员工",
        "统计各部门的员工数量",
        "查询工资最高的前5名员工",
        "查询IT部门的员工",
        "统计全公司的平均工资"
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example}")
    
    print("\n" + "=" * 70)
    print("📚 更多信息")
    print("=" * 70)
    print("• 详细文档: README.md")
    print("• 使用指南: USAGE_GUIDE.md")
    print("• 项目总结: PROJECT_SUMMARY.md")
    print("• 测试脚本: test.py")
    print("• 演示脚本: demo.py")
    print("• 交互程序: main.py")
    
    print("\n" + "=" * 70)
    print("✅ 准备完成！现在可以开始使用数据库Agent助手了")
    print("=" * 70)
    
    return True


if __name__ == "__main__":
    success = quick_start()
    if not success:
        print("\n❌ 快速开始检查失败，请解决上述问题后重试")
        exit(1)
    else:
        print("\n🎉 恭喜！所有检查通过，可以开始使用了")