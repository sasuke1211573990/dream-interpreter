#!/usr/bin/env python3
"""
测试AI服务是否正常工作 - 超简化版
"""
import requests
import json

def test_ai_service():
    """测试AI服务"""
    print("🧪 测试AI服务...")
    
    try:
        # 测试健康检查
        health_url = "http://127.0.0.1:5000/health"
        response = requests.get(health_url, timeout=10)
        print(f"健康检查状态: {response.status_code}")
        print(f"健康检查响应: {response.json()}")
        
        # 测试梦境解析 - 使用更简单的请求
        api_url = "http://127.0.0.1:5000/interpret"
        test_data = {
            "text": "蛇"
        }
        
        print("\n🧠 测试梦境解析API...")
        print(f"发送请求到: {api_url}")
        print(f"请求数据: {test_data}")
        
        response = requests.post(api_url, json=test_data, timeout=60)
        print(f"API状态: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"解析结果: {result}")
            return True
        else:
            print(f"API错误: {response.text}")
            return False
            
    except requests.exceptions.Timeout as e:
        print(f"❌ 请求超时: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_ai_service()
    if success:
        print("\n🎉 AI服务测试成功!")
    else:
        print("\n💥 AI服务测试失败!")