#!/usr/bin/env python3
"""
快速测试AI服务 - 调整max_new_tokens参数 (优化版)
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from service import DreamInterpreter

def test_direct_service():
    """直接测试服务类 - 使用较小的max_new_tokens"""
    print("🧪 快速测试DreamInterpreter服务...")
    
    try:
        # 设置较小的max_new_tokens来加快生成速度
        os.environ["MAX_NEW_TOKENS"] = "50"  # 从256减少到50
        print("⚙️ 设置max_new_tokens=50来加快生成速度")
        
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
        print("\n🎉 快速测试成功!")
    else:
        print("\n💥 快速测试失败!")