import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class DreamInterpreter:
    def __init__(self):
        # Prefer Hugging Face 国内镜像，如果外部网络不稳定可以提高成功率
        os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")
        os.environ.setdefault("HF_HUB_BASE_URL", "https://hf-mirror.com")

        self.model_name = os.environ.get("MODEL_NAME", "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B")
        print(f"Loading model {self.model_name} from {os.environ.get('HF_ENDPOINT')} ...")

        print("Loading tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True,
        )

        if torch.cuda.is_available():
            print(f"CUDA available. GPU: {torch.cuda.get_device_name(0)}")
        else:
            print("CUDA not available, using CPU")

        print("Loading model (this may take a while)...")
        load_kwargs = {
            "trust_remote_code": True,
        }
        if torch.cuda.is_available():
            load_kwargs["torch_dtype"] = torch.float16
            load_kwargs["device_map"] = "auto"
        else:
            load_kwargs["torch_dtype"] = torch.float32

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            **load_kwargs,
        )
        if not torch.cuda.is_available():
            self.model = self.model.to("cpu")

        print("Model loaded successfully.")
    
    def interpret(self, text):
        messages = [
            {"role": "user", "content": f"请帮我详细解析这个梦境，并给出心理学建议：\n{text}"}
        ]
        
        text_input = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        
        device = next(self.model.parameters()).device
        model_inputs = self.tokenizer(
            [text_input],
            return_tensors="pt",
            padding=True,
        ).to(device)

        max_new_tokens = int(os.environ.get("MAX_NEW_TOKENS", "256"))

        generated_ids = self.model.generate(
            input_ids=model_inputs.input_ids,
            attention_mask=model_inputs.attention_mask,
            max_new_tokens=max_new_tokens,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id,
        )
        
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return response

if __name__ == "__main__":
    interpreter = DreamInterpreter()
    print("Enter a dream to interpret (Ctrl+C to exit):")
    try:
        while True:
            dream = input("> ")
            if dream.strip():
                print("Interpreting (DeepSeek R1)...")
                result = interpreter.interpret(dream)
                print(f"\nResult:\n{result}\n")
    except KeyboardInterrupt:
        print("\nExiting...")
