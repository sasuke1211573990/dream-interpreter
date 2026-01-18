#!/usr/bin/env python3
"""
本地模型加载测试脚本
用于验证本地DeepSeek 7B模型是否能正常加载
"""

import os
import torch
import sys
from transformers import AutoModelForCausalLM, AutoTokenizer

def test_local_model_loading():
    """测试本地模型加载"""
    print("🔍 开始测试本地模型加载...")
    
    # 常见的本地模型存储路径
    possible_paths = [
        # Windows常见路径
        "C:\\Users\\%USERNAME%\\.cache\\huggingface\\hub\\models--deepseek-ai--DeepSeek-R1-Distill-Qwen-7B",
        "D:\\models\\deepseek-ai\\DeepSeek-R1-Distill-Qwen-7B",
        "E:\\models\\deepseek-ai\\DeepSeek-R1-Distill-Qwen-7B",
        os.path.expanduser("~\\.cache\\huggingface\\hub\\models--deepseek-ai--DeepSeek-R1-Distill-Qwen-7B"),
        # 相对路径
        "./models/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
        "../models/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
    ]
    
    # 扩展环境变量
    for i, path in enumerate(possible_paths):
        possible_paths[i] = os.path.expandvars(path)
    
    print("📁 检查可能的模型路径:")
    found_path = None
    for path in possible_paths:
        print(f"  检查: {path}")
        if os.path.exists(path):
            print(f"  ✅ 找到模型目录: {path}")
            found_path = path
            break
        else:
            print(f"  ❌ 路径不存在")
    
    if not found_path:
        print("\n❌ 未找到本地DeepSeek 7B模型文件")
        print("\n💡 建议:")
        print("1. 请确认模型文件下载位置")
        print("2. 设置 MODEL_PATH 环境变量指向模型目录")
        print("3. 或者将模型文件放置在以下位置之一:")
        for path in possible_paths:
            print(f"   - {path}")
        return False
    
    print(f"\n🧪 尝试加载模型: {found_path}")
    
    try:
        # 测试分词器加载
        print("📚 加载分词器...")
        tokenizer = AutoTokenizer.from_pretrained(
            found_path,
            trust_remote_code=True,
            local_files_only=True
        )
        print("✅ 分词器加载成功")
        
        # 测试模型加载
        print("🧠 加载模型...")
        load_kwargs = {
            "trust_remote_code": True,
            "local_files_only": True,
        }
        
        if torch.cuda.is_available():
            load_kwargs["torch_dtype"] = torch.float16
            load_kwargs["device_map"] = "auto"
            print(f"🎮 使用GPU: {torch.cuda.get_device_name(0)}")
        else:
            load_kwargs["torch_dtype"] = torch.float32
            print("💻 使用CPU模式")
        
        model = AutoModelForCausalLM.from_pretrained(
            found_path,
            **load_kwargs
        )
        
        print("✅ 模型加载成功")
        
        # 测试推理
        print("\n🧪 测试推理功能...")
        test_text = "你好，这是一个测试"
        messages = [{"role": "user", "content": test_text}]
        
        text_input = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        
        inputs = tokenizer(text_input, return_tensors="pt")
        
        if torch.cuda.is_available():
            inputs = {k: v.cuda() for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=50,
                do_sample=True,
                temperature=0.7,
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id,
            )
        
        response = tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)
        print(f"✅ 推理测试成功，响应: {response[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 模型加载失败: {e}")
        print(f"错误类型: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_local_model_loading()
    sys.exit(0 if success else 1)