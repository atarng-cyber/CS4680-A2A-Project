# server/handlers.py


async def handle_task(request) -> str:
    text_parts = [
        p.text for p in request.message.parts
        if getattr(p, 'type', None) == 'text'
    ]
    combined = ' '.join(text_parts)

    if combined.startswith('!summarise'):
        msg = "This is a 1-sentence mock summary of your text."
        return msg

    return combined