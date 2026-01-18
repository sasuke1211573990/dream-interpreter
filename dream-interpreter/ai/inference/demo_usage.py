#!/usr/bin/env python3
"""
梦境解析服务演示脚本
展示如何使用API进行梦境解析
"""
import requests
import json
import time

def test_health_check():
    """测试服务健康状态"""
    print("🏥 检查服务健康状态...")
    try:
        response = requests.get("http://127.0.0.1:5000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 服务状态: {data['status']}")
            print(f"✅ 模型加载: {data['model_loaded']}")
            return True
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return False

def interpret_dream(dream_text, max_tokens=None):
    """解析梦境"""
    print(f"\n🌙 解析梦境: {dream_text}")
    
    # 设置环境变量来调整生成参数（可选）
    if max_tokens:
        print(f"⚙️ 设置max_new_tokens={max_tokens}")
    
    data = {
        "text": dream_text
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            "http://127.0.0.1:5000/interpret", 
            json=data, 
            timeout=300  # 5分钟超时
        )
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            interpretation = result.get('interpretation', '无解析结果')
            
            print(f"✅ 解析完成！耗时: {end_time - start_time:.2f}秒")
            print(f"\n💭 梦境解析结果:")
            print("-" * 50)
            print(interpretation)
            print("-" * 50)
            
            return interpretation
        else:
            error_msg = response.json().get('error', '未知错误')
            print(f"❌ 解析失败: {error_msg}")
            return None
            
    except requests.exceptions.Timeout:
        print("❌ 请求超时 - 梦境解析需要较长时间")
        return None
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return None

def main():
    """主演示函数"""
    print("🌟 梦境解析AI服务演示")
    print("=" * 50)
    
    # 1. 检查服务状态
    if not test_health_check():
        print("❌ 服务未就绪，请确保app.py正在运行")
        return
    
    print("\n" + "=" * 50)
    
    # 2. 演示不同的梦境解析
    test_dreams = [
        "我梦见自己在飞翔",
        "梦见一条黑色的蛇",
        "梦见掉牙齿",
        "梦见考试不及格"
    ]
    
    for i, dream in enumerate(test_dreams, 1):
        print(f"\n📝 测试案例 {i}/{len(test_dreams)}")
        interpret_dream(dream)
        
        if i < len(test_dreams):
            input("\n按回车键继续下一个测试...")
    
    print("\n🎉 演示完成！")
    
    # 3. 交互模式
    print("\n" + "=" * 50)
    print("💬 交互模式 - 输入您的梦境进行解析")
    print("输入 'quit' 或 '退出' 结束")
    print("=" * 50)
    
    while True:
        user_input = input("\n🌙 请输入您的梦境: ").strip()
        
        if user_input.lower() in ['quit', 'exit', '退出', '结束']:
            print("👋 感谢您的使用！")
            break
            
        if not user_input:
            continue
            
        # 询问是否调整参数
        print("\n⚙️ 选项:")
        print("1. 快速解析 (约2-3分钟)")
        print("2. 标准解析 (约5-8分钟)")  
        print("3. 详细解析 (约10-15分钟)")
        choice = input("请选择解析模式 (1-3，默认2): ").strip()
        
        # 根据选择设置参数
        if choice == '1':
            os.environ["MAX_NEW_TOKENS"] = "20"
        elif choice == '3':
            os.environ["MAX_NEW_TOKENS"] = "100"
        else:
            os.environ["MAX_NEW_TOKENS"] = "50"  # 默认标准模式
            
        interpret_dream(user_input)

if __name__ == "__main__":
    main()