#!/usr/bin/env python3
"""
测试AI服务是否正常工作 - 直接调用service.py (简化版)
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from service import DreamInterpreter

def test_direct_service():
    """直接测试服务类"""
    print("🧪 直接测试DreamInterpreter服务...")
    
    try:
        # 创建解释器实例
        print("正在创建DreamInterpreter实例...")
        interpreter = DreamInterpreter(verbose=True)
        
        # 测试梦境解析 - 使用简单的文本
        test_text = "蛇"
        print(f"\n🧠 测试梦境解析: {test_text}")
        
        result = interpreter.interpret(test_text)
        print(f"\n解析结果: {result}")
        
        # 打印推理过程
        interpreter.print_inference_summary()
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_direct_service()
    if success:
        print("\n🎉 直接服务测试成功!")
    else:
        print("\n💥 直接服务测试失败!")