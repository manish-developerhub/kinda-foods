#!/usr/bin/env python3
"""
AI-backed chatbot script.

Behavior:
- If the environment variable OPENAI_API_KEY is set, the script will use OpenAI's ChatCompletion API
  to generate responses.
- If OPENAI_API_KEY is not set or OpenAI calls fail, the script falls back to a small rule-based
  responder so the chatbot remains usable offline.

Usage (PowerShell):
  python -m pip install -r requirements.txt
  $env:OPENAI_API_KEY = '<your_api_key>'  # optional - only required for AI responses
  python chatbot.py

Replace <your_api_key> with your OpenAI API key if you want AI responses.
"""

import os
import sys

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

def local_response(user_text: str) -> str:
    """A small rule-based fallback responder."""
    t = user_text.lower()
    if any(g in t for g in ('hi', 'hello', 'hey')):
        return "Hello! I'm here to help — what's on your mind?"
    if 'how are you' in t:
        return "I'm a script, but I'm functioning correctly — thanks!"
    if 'name' in t:
        return "You can call me KindaBot — your site assistant."
    if 'menu' in t or 'food' in t or 'order' in t:
        return "You can browse our menu on the website. If you'd like, tell me what you'd like to order and I'll place the order for you."
    if 'bye' in t or 'exit' in t or 'quit' in t:
        return "Goodbye! Have a great day!"
    return "Sorry, I don't understand fully yet. Can you rephrase?"


def ai_response(openai, user_text: str) -> str:
    """Call OpenAI ChatCompletion (gpt-3.5-turbo) to get a response."""
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for a food delivery website. Keep answers brief and friendly."},
                {"role": "user", "content": user_text}
            ],
            max_tokens=200,
            temperature=0.7,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        # On any error, return a message so we can fallback gracefully
        return f"(AI error) {e}"


def main():
    print("Hello — KindaBot here. Type 'bye' to exit.")

    if OPENAI_API_KEY:
        try:
            import openai
            openai.api_key = OPENAI_API_KEY
            use_ai = True
            print("AI mode: enabled (using OpenAI)")
        except Exception as e:
            print(f"Failed to import openai package: {e}. Falling back to local responder.")
            use_ai = False
    else:
        use_ai = False
        print("AI mode: disabled (no OPENAI_API_KEY). Using local responder.")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print('\nGoodbye!')
            sys.exit(0)

        if not user_input:
            continue

        if user_input.lower() in ('bye', 'exit', 'quit'):
            print('KindaBot: Goodbye!')
            break

        if use_ai:
            # Try AI first
            resp = ai_response(openai, user_input)
            if resp.startswith('(AI error)'):
                # fallback
                print('KindaBot (fallback):', local_response(user_input))
            else:
                print('KindaBot:', resp)
        else:
            print('KindaBot:', local_response(user_input))


if __name__ == '__main__':
    main()
