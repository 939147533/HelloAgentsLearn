"""
数据库Agent助手 - 简单演示脚本
展示基本功能的使用方法
"""
import os
from dotenv import load_dotenv
from hello_agents import HelloAgentsLLM
from database_agent import DatabaseAgent, DatabaseConfig

load_dotenv()


def demo_basic_query():
    """演示基本查询功能"""
    print("=" * 60)
    print("🎯 数据库Agent助手 - 功能演示")
    print("=" * 60)
    
    # 初始化LLM
    print("\n1️⃣ 初始化LLM...")
    llm = HelloAgentsLLM(
        model=os.getenv("LLM_MODEL_ID", "Qwen/Qwen2.5-7B-Instruct"),
        apiKey=os.getenv("LLM_API_KEY"),
        baseUrl=os.getenv("LLM_BASE_URL")
    )
    print("✅ LLM初始化完成")
    
    # 配置数据库
    print("\n2️⃣ 配置数据库连接...")
    db_config = DatabaseConfig(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "1521")),
        service_name=os.getenv("DB_SERVICE_NAME", "ORCL"),
        username=os.getenv("DB_USERNAME", "system"),
        password=os.getenv("DB_PASSWORD")
    )
    
    if not db_config.validate():
        print("❌ 数据库配置不完整，请检查.env文件")
        return
    
    print(f"✅ 数据库配置完成: {db_config.host}:{db_config.port}/{db_config.service_name}")
    
    # 创建Agent
    print("\n3️⃣ 创建DatabaseAgent...")
    agent = DatabaseAgent(
        name="DatabaseAssistant",
        llm=llm,
        db_config=db_config,
        max_steps=5
    )
    print("✅ Agent创建完成")
    
    # 演示查询
    print("\n4️⃣ 执行演示查询...")
    
    demo_queries = [
        "查询数据库中有哪些表",
        "查询所有员工信息",
        "查询工资最高的前3名员工",
        "统计各部门的员工数量"
    ]
    
    for i, query in enumerate(demo_queries, 1):
        print(f"\n{'=' * 60}")
        print(f"演示查询 {i}: {query}")
        print('=' * 60)
        
        try:
            result = agent.run(query)
            print(f"\n📊 查询结果:\n{result}")
        except Exception as e:
            print(f"❌ 查询执行失败: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 演示完成！")
    print("=" * 60)


def demo_interactive():
    """演示交互式查询"""
    print("=" * 60)
    print("🎯 数据库Agent助手 - 交互式演示")
    print("=" * 60)
    
    # 初始化
    llm = HelloAgentsLLM(
        model=os.getenv("LLM_MODEL_ID"),
        apiKey=os.getenv("LLM_API_KEY"),
        baseUrl=os.getenv("LLM_BASE_URL")
    )
    
    db_config = DatabaseConfig()
    
    if not db_config.validate():
        print("❌ 数据库配置不完整")
        return
    
    agent = DatabaseAgent(
        name="InteractiveAssistant",
        llm=llm,
        db_config=db_config,
        max_steps=5
    )
    
    print("\n💡 提示: 输入您的自然语言查询，输入 'quit' 退出")
    print("-" * 60)
    
    while True:
        user_input = input("\n🔍 请输入查询: ").strip()
        
        if user_input.lower() in ['quit', 'exit', '退出']:
            print("👋 再见！")
            break
        
        if not user_input:
            continue
        
        try:
            result = agent.run(user_input)
            print(f"\n📊 查询结果:\n{result}")
        except Exception as e:
            print(f"❌ 查询执行失败: {e}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        demo_interactive()
    else:
        demo_basic_query()