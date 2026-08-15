"""Resolve ambiguous follow-up queries into self-contained ones.

Problem this solves: a user might ask "How much did I spend on food in
June?" then follow up with just "What about July?". Taken alone, the
follow-up has no category in it -- intent_router.py and finance_agent.py
would happily process it as a plain MONTHLY_SPEND query for the WHOLE
month, silently dropping the "food" constraint the user clearly still
means.

This module asks the LLM to rewrite a query using prior conversation
turns ONLY when needed, producing a self-contained query that can then go
through the existing detect_intent() -> run_finance_agent() pipeline
completely unchanged. No other file needs to change.

Design choices:
- If there's no history yet (first message in a session), skip the LLM
  call entirely and return the query as-is -- there's nothing to
  disambiguate against, and this saves a Groq call on every
  conversation's first turn.
- The rewrite prompt is explicitly told to leave already-self-contained
  queries untouched, to avoid introducing drift into queries that don't
  need history at all.
- This is a SEPARATE Groq call from intent classification
  (agents/intent_router.py). Conversation memory and intent detection are
  deliberately kept as two independent concerns, per the design we agreed
  on: classification looks at the single (now-rewritten) query only;
  history is used here, before classification, not during it.
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


REWRITE_PROMPT = """You rewrite a user's latest message into a fully self-contained question, using the conversation history ONLY if the latest message is ambiguous or missing context (like a category, date, or item mentioned earlier).

Rules:
- If the latest message already makes complete sense on its own, return it EXACTLY as-is, unchanged.
- If the latest message is a follow-up that depends on something mentioned earlier (a category, an item, a price, a date range), rewrite it to include that missing context explicitly.
- Do NOT answer the question. Do NOT add information that wasn't in the history or the message. Only fill in what's missing.
- Reply with ONLY the rewritten question, nothing else -- no explanation, no quotes.

Conversation history:
{history}

Latest message: "{query}"

Rewritten self-contained question:"""


def resolve_query(query, history):
    """Return a self-contained version of `query`, using `history` if needed.

    `history` is expected to be the same kind of newline-joined
    "role: content" string chatbot.py already builds. If history is empty
    (first message of a session), the query is returned unchanged and no
    API call is made.
    """
    if not history or not history.strip():
        return query

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0,  # deterministic rewriting, not creative text
            max_tokens=200,
            messages=[
                {
                    "role": "user",
                    "content": REWRITE_PROMPT.format(history=history, query=query),
                }
            ],
        )
        rewritten = (response.choices[0].message.content or "").strip()
        # Strip accidental wrapping quotes the model sometimes adds despite
        # being told not to.
        rewritten = rewritten.strip('"').strip("'")
        return rewritten if rewritten else query
    except Exception as e:
        print(f"Warning: query rewrite failed ({e}); using original query")
        return query