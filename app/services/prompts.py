DEFAULT_PROMPTS = {
    "classify": "Classify the following text into one of these categories: {categories}.\nText: {text}\nCategory:",
    "summarize": "Summarize the following text in a concise manner:\n\n{text}\n\nSummary:",
    "extract_fields": "Extract the following fields from the text: {fields}.\nText: {text}\nReturn the result as a JSON object.",
    "generate_reply": "Generate a reply to the following context using a {tone} tone.\nContext: {context}\nReply:"
}

def get_prompt(action_type: str, custom_template: str = None, **kwargs) -> str:
    template = custom_template if custom_template else DEFAULT_PROMPTS.get(action_type)
    if not template:
        raise ValueError(f"No template found for action {action_type}")
    
    try:
        return template.format(**kwargs)
    except KeyError as e:
        raise ValueError(f"Missing required prompt variable: {e}")
