import os
import torch
import time
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoConfig
from typing import Optional, List, Dict

class DreamInterpreter:
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.loading_steps = []
        self.inference_steps = []
        self.model = None
        self.tokenizer = None
        self.use_llm = False
        
        os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")
        os.environ.setdefault("HF_HUB_BASE_URL", "https://hf-mirror.com")
        for k in ["HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"]:
            if k in os.environ:
                os.environ.pop(k)

        # 检查本地模型路径
        local_model_path = self._find_local_model()
        if local_model_path:
            self.model_name = local_model_path
            self._log_step(f"🎯 使用本地模型: {local_model_path}")
        else:
            self.model_name = os.environ.get("MODEL_NAME", "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B")
            self._log_step(f"🌐 使用远程模型: {self.model_name}")
        
        try:
            self._log_step(f"🚀 开始加载模型: {self.model_name}")
            self._log_step(f"📡 使用镜像: {os.environ.get('HF_ENDPOINT')}")

            self._log_step("📚 正在加载分词器...")
            start_time = time.time()
            
            # 首先检查模型配置
            config = AutoConfig.from_pretrained(
                self.model_name,
                trust_remote_code=True,
                local_files_only=local_model_path is not None
            )
            self._log_step(f"🔍 模型类型: {config.model_type}")
            
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True,
                local_files_only=local_model_path is not None
            )
            load_time = time.time() - start_time
            self._log_step(f"✅ 分词器加载完成 (耗时: {load_time:.2f}s)")

            if torch.cuda.is_available():
                self._log_step(f"🎮 CUDA可用，GPU: {torch.cuda.get_device_name(0)}")
            else:
                self._log_step("💻 使用CPU模式")

            self._log_step("🧠 正在加载模型(这可能需要一些时间)...")
            start_time = time.time()
            load_kwargs = {
                "trust_remote_code": True,
                "local_files_only": local_model_path is not None,
            }
            if torch.cuda.is_available():
                load_kwargs["torch_dtype"] = torch.float16
                load_kwargs["device_map"] = "auto"
            else:
                load_kwargs["torch_dtype"] = torch.float32

            # 根据模型类型选择合适的加载方式
            if config.model_type == "qwen2":
                from transformers import Qwen2ForCausalLM
                self.model = Qwen2ForCausalLM.from_pretrained(
                    self.model_name,
                    **load_kwargs,
                )
            else:
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    **load_kwargs,
                )
            if not torch.cuda.is_available():
                self.model = self.model.to("cpu")
            load_time = time.time() - start_time
            self._log_step(f"✅ 模型加载完成 (耗时: {load_time:.2f}s)")
            self.use_llm = True
        
            if hasattr(self.model, 'config'):
                self._log_step(f"📊 模型参数: {getattr(self.model.config, 'n_parameters', '未知')}")
                self._log_step(f"📝 词汇表大小: {getattr(self.model.config, 'vocab_size', '未知')}")
        except Exception as e:
            self._log_step(f"❌ 模型加载失败，将使用规则引擎: {e}")

    def _find_local_model(self) -> Optional[str]:
        """查找本地DeepSeek模型路径"""
        possible_paths = [
            # Windows常见路径
            os.path.expanduser("~\\.cache\\huggingface\\hub\\models--deepseek-ai--DeepSeek-R1-Distill-Qwen-7B\\snapshots"),
            "D:\\models\\deepseek-ai\\DeepSeek-R1-Distill-Qwen-7B",
            "E:\\models\\deepseek-ai\\DeepSeek-R1-Distill-Qwen-7B",
            "./models/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
            "../models/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
        ]
        
        for base_path in possible_paths:
            if os.path.exists(base_path):
                if "snapshots" in base_path:
                    # 如果是snapshots目录，查找最新版本
                    try:
                        subdirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
                        if subdirs:
                            latest_snapshot = os.path.join(base_path, sorted(subdirs)[-1])
                            config_path = os.path.join(latest_snapshot, "config.json")
                            if os.path.exists(config_path):
                                return latest_snapshot
                    except Exception:
                        pass
                else:
                    # 直接检查模型目录
                    config_path = os.path.join(base_path, "config.json")
                    if os.path.exists(config_path):
                        return base_path
        
        return None

    def _log_step(self, message: str):
        if self.verbose:
            print(f"[{time.strftime('%H:%M:%S')}] {message}")
        self.loading_steps.append(message)
    
    def _log_inference(self, message: str):
        if self.verbose:
            print(f"🤔 {message}")
        self.inference_steps.append(message)
    
    def interpret(self, text: str) -> str:
        self.inference_steps = []  # 清空之前的推理步骤
        
        self._log_inference(f"📝 收到梦境描述: {text[:50]}{'...' if len(text) > 50 else ''}")
        if not self.model or not self.tokenizer or not self.use_llm:
            self._log_inference("⚠️ 未加载大模型，使用规则引擎进行解析")
            return self._fallback_interpret(text)
        
        messages = [
            {"role": "user", "content": f"请帮我详细解析这个梦境，并给出心理学建议：\n{text}"}
        ]
        
        self._log_inference("🔧 正在构建输入模板...")
        text_input = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        self._log_inference(f"📄 输入模板长度: {len(text_input)} 字符")
        
        # 分词
        self._log_inference("🔍 正在对输入进行分词...")
        device = next(self.model.parameters()).device
        model_inputs = self.tokenizer(
            [text_input],
            return_tensors="pt",
            padding=True,
        ).to(device)
        
        input_length = model_inputs.input_ids.shape[1]
        self._log_inference(f"📊 输入token数量: {input_length}")
        
        # 设置生成参数
        max_new_tokens = int(os.environ.get("MAX_NEW_TOKENS", "256"))
        self._log_inference(f"⚙️ 生成参数设置: max_new_tokens={max_new_tokens}, temperature=0.7, top_p=0.9")
        
        # 开始生成
        self._log_inference("🚀 开始生成回复...")
        start_time = time.time()
        
        # 使用更详细的生成过程
        generated_ids = self.model.generate(
            input_ids=model_inputs.input_ids,
            attention_mask=model_inputs.attention_mask,
            max_new_tokens=max_new_tokens,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id,
            # 添加回调函数来显示生成进度
            output_scores=True,
            return_dict_in_generate=True,
        )
        
        generation_time = time.time() - start_time
        
        # 处理生成的ID
        generated_ids_output = generated_ids.sequences
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids_output)
        ]
        
        output_length = len(generated_ids[0])
        self._log_inference(f"✅ 生成完成!")
        self._log_inference(f"📏 输出token数量: {output_length}")
        self._log_inference(f"⏱️ 生成耗时: {generation_time:.2f}秒")
        self._log_inference(f"⚡ 生成速度: {output_length/generation_time:.2f} tokens/秒")

        # 解码
        self._log_inference("🔤 正在解码输出...")
        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        self._log_inference(f"📤 最终回复长度: {len(response)} 字符")
        
        return response

    def _fallback_interpret(self, text: str) -> str:
        self._log_inference("开始分析梦境关键词")
        lower = text.lower()
        analysis_parts = []
        if "蛇" in text or "snake" in lower:
            analysis_parts.append("梦到蛇往往和潜意识中的紧张、压力或者对未知的担忧有关。")
        if "追" in text or "追赶" in text or "chase" in lower:
            analysis_parts.append("被追赶通常代表你在现实中有想逃避的问题或压力。")
        if "掉" in text or "坠落" in text or "fall" in lower:
            analysis_parts.append("下坠感经常和不安全感、对未来的不确定有关。")
        if "考试" in text or "test" in lower or "考试" in text:
            analysis_parts.append("考试场景多和自我要求、焦虑以及对评价的担心相关。")
        if not analysis_parts:
            analysis_parts.append("这个梦境反映出你最近情绪上存在一定的紧张和不安。")
        self._log_inference("综合情节和情绪进行整体判断")
        interpretation = "梦境解析：\n" + "\n".join(f"- {p}" for p in analysis_parts)
        suggestion = "\n\n心理建议：\n- 建议你留意最近让你感到紧张或被追赶的事情。\n- 可以通过记录情绪、和信任的人沟通来释放压力。\n- 保持规律作息和适度放松，有助于减轻这类梦境带来的影响。"
        return interpretation + suggestion

    def print_inference_summary(self):
        print("\n" + "="*60)
        print("🧠 推理过程总结:")
        print("="*60)
        for i, step in enumerate(self.inference_steps, 1):
            print(f"{i:2d}. {step}")
        print("="*60)
        
    def get_model_info(self) -> Dict:
        return {
            "model_name": self.model_name,
            "device": str(next(self.model.parameters()).device) if self.model is not None else "cpu",
            "loading_steps": self.loading_steps,
            "total_loading_steps": len(self.loading_steps)
        }

if __name__ == "__main__":
    print("🌙 梦境解析AI助手 (DeepSeek-R1)")
    print("="*60)
    
    interpreter = DreamInterpreter(verbose=True)
    
    print("\n✨ 模型加载完成！可以开始解析梦境了")
    print("💡 提示：输入您的梦境描述，我会为您详细解析")
    print("🔄 输入 'info' 查看模型信息")
    print("📊 输入 'summary' 查看推理过程总结")
    print("❌ 输入 'exit' 或按 Ctrl+C 退出")
    print("="*60)
    
    try:
        while True:
            dream = input("\n📝 请输入您的梦境描述 > ").strip()
            
            if not dream:
                continue
                
            if dream.lower() == 'exit':
                print("👋 感谢使用，再见！")
                break
            elif dream.lower() == 'info':
                info = interpreter.get_model_info()
                print(f"\n📊 模型信息:")
                print(f"   模型名称: {info['model_name']}")
                print(f"   运行设备: {info['device']}")
                print(f"   加载步骤: {info['total_loading_steps']} 步")
                continue
            elif dream.lower() == 'summary':
                interpreter.print_inference_summary()
                continue
            
            print(f"\n🔮 正在解析您的梦境...")
            print("-" * 40)
            
            try:
                result = interpreter.interpret(dream)
                
                print("\n" + "="*60)
                print("🌟 梦境解析结果:")
                print("="*60)
                print(result)
                print("="*60)
                
                # 显示推理总结
                interpreter.print_inference_summary()
                
            except Exception as e:
                print(f"❌ 解析过程中出现错误: {e}")
                print("💡 请检查输入或稍后重试")
                
    except KeyboardInterrupt:
        print("\n\n👋 感谢使用梦境解析AI助手，再见！")
