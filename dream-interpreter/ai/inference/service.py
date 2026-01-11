from transformers import pipeline

class DreamInterpreter:
    def __init__(self):
        # Using a smaller model for faster download/inference in dev environment
        # gpt2-medium is ~1.5GB. distilgpt2 is smaller.
        # But sticking to user request: gpt2-medium
        print("Loading model...")
        self.model = pipeline('text-generation', model='gpt2-medium')
        print("Model loaded.")
    
    def interpret(self, text):
        prompt = f"解释这个梦境：{text}\n解析："
        # max_length should include input length
        return self.model(prompt, max_length=200, num_return_sequences=1)[0]['generated_text']

if __name__ == "__main__":
    interpreter = DreamInterpreter()
    print("Enter a dream to interpret (Ctrl+C to exit):")
    try:
        while True:
            dream = input("> ")
            if dream.strip():
                print("Interpreting...")
                result = interpreter.interpret(dream)
                print(f"\nResult:\n{result}\n")
    except KeyboardInterrupt:
        print("\nExiting...")
