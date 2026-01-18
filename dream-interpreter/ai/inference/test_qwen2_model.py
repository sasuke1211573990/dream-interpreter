#!/usr/bin/env python3
"""
测试Qwen2模型加载
"""
import os
import torch
from transformers import AutoTokenizer, AutoConfig
from transformers import Qwen2ForCausalLM

def test_qwen2_loading():
    """测试Qwen2模型加载"""
    print("🚀 开始测试Qwen2模型加载...")
    
    # 本地模型路径
    model_path = r"C:\Users\ZhuanZ(无密码)\.cache\huggingface\hub\models--deepseek-ai--DeepSeek-R1-Distill-Qwen-7B\snapshots\916b56a44061fd5cd7d6a8fb632557ed4f724f60"
    
    try:
        print(f"📁 模型路径: {model_path}")
        
        # 检查模型配置
        print("🔍 加载模型配置...")
        config = AutoConfig.from_pretrained(model_path, trust_remote_code=True, local_files_only=True)
        print(f"✅ 模型类型: {config.model_type}")
        print(f"✅ 模型架构: {config.architectures}")
        
        # 加载分词器
        print("📚 加载分词器...")
        tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True, local_files_only=True)
        print(f"✅ 分词器加载成功")
        
        # 加载模型
        print("🧠 加载Qwen2模型...")
        model = Qwen2ForCausalLM.from_pretrained(
            model_path,
            trust_remote_code=True,
            local_files_only=True,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None,
        )
        
        if not torch.cuda.is_available():
            model = model.to("cpu")
            
        print("✅ 模型加载成功!")
        
        # 简单测试
        print("🧪 进行推理测试...")
        test_text = "梦见蛇是什么意思？"
        inputs = tokenizer(test_text, return_tensors="pt")
        
        if torch.cuda.is_available():
            inputs = {k: v.cuda() for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = model.generate(**inputs, max_length=100, num_return_sequences=1)
        
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"📝 测试结果: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_qwen2_loading()
    if success:
        print("\n🎉 Qwen2模型加载测试成功!")
    else:
        print("\n💥 Qwen2模型加载测试失败!")