#!/usr/bin/env python3
"""
模型文件哈希校验工具
"""
import os
import hashlib
import json
from pathlib import Path
from typing import Dict, List, Optional

def calculate_file_hash(file_path: str, algorithm: str = "sha256") -> str:
    """计算文件的哈希值"""
    hash_obj = hashlib.new(algorithm)
    
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    except Exception as e:
        print(f"计算哈希失败 {file_path}: {e}")
        return ""

def find_model_files(model_path: str) -> List[str]:
    """查找模型相关文件"""
    model_files = []
    
    if not os.path.exists(model_path):
        return model_files
    
    # 常见模型文件扩展名
    model_extensions = [".bin", ".safetensors", ".pt", ".pth", ".ckpt"]
    
    # 检查目录中的文件
    for root, dirs, files in os.walk(model_path):
        for file in files:
            file_path = os.path.join(root, file)
            
            # 包含模型文件扩展名或者是重要配置文件
            if any(file.endswith(ext) for ext in model_extensions) or \
               file in ["config.json", "tokenizer.json", "tokenizer_config.json", "pytorch_model.bin.index.json", "model.safetensors.index.json"]:
                model_files.append(file_path)
    
    return model_files

def verify_model_hashes(model_path: str, reference_hashes: Optional[Dict[str, str]] = None) -> Dict:
    """验证模型文件的哈希值"""
    print(f"🔍 正在扫描模型目录: {model_path}")
    
    model_files = find_model_files(model_path)
    
    if not model_files:
        print("❌ 未找到模型文件")
        return {"status": "error", "message": "未找到模型文件"}
    
    print(f"📁 找到 {len(model_files)} 个模型相关文件")
    
    results = {
        "model_path": model_path,
        "total_files": len(model_files),
        "hashes": {},
        "missing_files": [],
        "mismatched_files": [],
        "verified_files": []
    }
    
    # 计算所有文件的哈希值
    for file_path in model_files:
        file_name = os.path.basename(file_path)
        print(f"🔄 正在计算 {file_name} 的哈希值...")
        
        file_hash = calculate_file_hash(file_path)
        if file_hash:
            results["hashes"][file_name] = file_hash
            
            # 如果有参考哈希值，进行比对
            if reference_hashes and file_name in reference_hashes:
                if file_hash == reference_hashes[file_name]:
                    results["verified_files"].append(file_name)
                    print(f"✅ {file_name}: 哈希值匹配")
                else:
                    results["mismatched_files"].append(file_name)
                    print(f"❌ {file_name}: 哈希值不匹配")
            else:
                print(f"ℹ️  {file_name}: {file_hash[:16]}...")
    
    # 检查缺失的文件
    if reference_hashes:
        for ref_file in reference_hashes.keys():
            if ref_file not in [os.path.basename(f) for f in model_files]:
                results["missing_files"].append(ref_file)
                print(f"⚠️  缺失文件: {ref_file}")
    
    # 总体状态
    if reference_hashes:
        if not results["mismatched_files"] and not results["missing_files"]:
            results["status"] = "verified"
            print("\n🎉 所有文件哈希值验证通过!")
        else:
            results["status"] = "mismatch"
            print(f"\n⚠️  发现 {len(results['mismatched_files'])} 个文件哈希值不匹配, {len(results['missing_files'])} 个文件缺失")
    else:
        results["status"] = "calculated"
        print(f"\n✅ 已完成 {len(results['hashes'])} 个文件的哈希值计算")
    
    return results

def save_hashes_to_file(hashes: Dict[str, str], output_file: str):
    """保存哈希值到文件"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(hashes, f, indent=2, ensure_ascii=False)
        print(f"💾 哈希值已保存到: {output_file}")
    except Exception as e:
        print(f"❌ 保存哈希值失败: {e}")

def main():
    """主函数"""
    print("🔐 DeepSeek模型文件哈希校验工具")
    print("=" * 50)
    
    # 自动检测本地模型路径
    possible_paths = [
        os.path.expanduser("~\.cache\huggingface\hub\models--deepseek-ai--DeepSeek-R1-Distill-Qwen-7B\snapshots"),
        "D:\\models\\deepseek-ai\\DeepSeek-R1-Distill-Qwen-7B",
        "E:\\models\\deepseek-ai\\DeepSeek-R1-Distill-Qwen-7B",
        "./models/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
        "../models/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
    ]
    
    model_path = None
    for path in possible_paths:
        if os.path.exists(path):
            # 如果是snapshots目录，查找最新版本
            if "snapshots" in path:
                try:
                    subdirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
                    if subdirs:
                        latest_snapshot = os.path.join(path, sorted(subdirs)[-1])
                        config_path = os.path.join(latest_snapshot, "config.json")
                        if os.path.exists(config_path):
                            model_path = latest_snapshot
                            break
                except Exception:
                    pass
            else:
                config_path = os.path.join(path, "config.json")
                if os.path.exists(config_path):
                    model_path = path
                    break
    
    if not model_path:
        print("❌ 未找到本地DeepSeek模型")
        print("请手动指定模型路径，例如:")
        print("python verify_model_hashes.py --path /path/to/model")
        return
    
    print(f"📍 检测到模型路径: {model_path}")
    
    # 询问用户是否要保存哈希值
    save_hashes = input("是否保存计算出的哈希值到文件? (y/n): ").lower().strip() == 'y'
    
    # 执行哈希校验
    results = verify_model_hashes(model_path)
    
    # 保存结果
    if save_hashes and results["hashes"]:
        output_file = "deepseek_model_hashes.json"
        save_hashes_to_file(results["hashes"], output_file)
    
    # 显示总结
    print("\n" + "=" * 50)
    print("📊 校验结果总结:")
    print(f"模型路径: {model_path}")
    print(f"总文件数: {results['total_files']}")
    print(f"计算哈希: {len(results['hashes'])}")
    
    if results["status"] == "verified":
        print("✅ 所有文件验证通过")
    elif results["status"] == "mismatch":
        print(f"⚠️  {len(results['mismatched_files'])} 个文件不匹配")
        if results["mismatched_files"]:
            print("不匹配文件:")
            for f in results["mismatched_files"]:
                print(f"  - {f}")
    elif results["status"] == "calculated":
        print("✅ 哈希值计算完成")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="DeepSeek模型文件哈希校验工具")
    parser.add_argument("--path", type=str, help="模型目录路径")
    parser.add_argument("--reference", type=str, help="参考哈希值JSON文件")
    parser.add_argument("--output", type=str, help="输出哈希值到文件")
    
    args = parser.parse_args()
    
    if args.path:
        # 使用指定的路径
        reference_hashes = None
        if args.reference:
            try:
                with open(args.reference, 'r') as f:
                    reference_hashes = json.load(f)
            except Exception as e:
                print(f"❌ 读取参考哈希文件失败: {e}")
                sys.exit(1)
        
        results = verify_model_hashes(args.path, reference_hashes)
        
        if args.output:
            save_hashes_to_file(results["hashes"], args.output)
    else:
        # 交互模式
        main()