import os
from openai import OpenAI

client = OpenAI()

def run_arc_brain(prompt):

    system_prompt = """
You are ARC, the venue operating intelligence system.

Your job is to help venue operators understand what is happening in the room.

You speak clearly, briefly, and confidently.

You help operators manage:
- energy levels
- guest activity
- engagement
- event timing
- operational awareness

Always respond like a calm operations assistant.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":prompt}
        ],
        temperature=0.4
    )

    return response.choices[0].message.content
