
# Wire this into node.py where indicated if you want real completions.
# Example usage:
#   from adapter_examples.openai_adapter_stub import complete
#   result_text = complete(prompt, context)
def complete(prompt: str, context: dict) -> str:
    return f"OPENAI_STUB -> {prompt[:128]} | ctx={list(context.keys())}"
