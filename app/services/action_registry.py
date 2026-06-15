from app.services.openai_client import openai_client
from app.services.connectors.slack import slack_connector
from app.services.connectors.email import email_connector
from app.services.connectors.http import http_connector

# Wrapper functions for AI so they match the connector signature if we want, or just handle them separately.
# AI actions don't strictly need config from DB right now since we use OPENAI_API_KEY from env, but we keep the signature consistent.

async def ai_classify_handler(config, params, context_data):
    # Ignore config
    output, tokens = await openai_client.classify(params.get("text", ""), params.get("categories", ""), params.get("custom_template"))
    return output, tokens

async def ai_summarize_handler(config, params, context_data):
    output, tokens = await openai_client.summarize(params.get("text", ""), params.get("custom_template"))
    return output, tokens

async def ai_extract_fields_handler(config, params, context_data):
    output, tokens = await openai_client.extract_fields(params.get("text", ""), params.get("fields", ""), params.get("custom_template"))
    return output, tokens

async def ai_generate_reply_handler(config, params, context_data):
    output, tokens = await openai_client.generate_reply(params.get("context", ""), params.get("tone", "neutral"), params.get("custom_template"))
    return output, tokens

# Standard connector wrapper
async def connector_handler(connector_obj, config, params, context_data):
    output = await connector_obj.execute(config, params, context_data)
    return output, 0 # 0 tokens used

ACTION_REGISTRY = {
    "slack.send": lambda c, p, ctx: connector_handler(slack_connector, c, p, ctx),
    "email.send": lambda c, p, ctx: connector_handler(email_connector, c, p, ctx),
    "http.request": lambda c, p, ctx: connector_handler(http_connector, c, p, ctx),
    "ai.classify": ai_classify_handler,
    "ai.summarize": ai_summarize_handler,
    "ai.extract_fields": ai_extract_fields_handler,
    "ai.generate_reply": ai_generate_reply_handler,
}

def get_action_handler(action_type: str):
    handler = ACTION_REGISTRY.get(action_type)
    if not handler:
        raise ValueError(f"Unsupported action type: {action_type}")
    return handler
