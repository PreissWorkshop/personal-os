#!/usr/bin/env python3
"""UserPromptSubmit hook: when a prompt mentions money, remind the model to
load the money skill before answering. Measured 2026-09-19: the skill's
description alone loaded it on only 2-3 of 10 casual money questions, so
this hook makes the trigger mechanical. A false positive costs one line of
context; a miss costs an answer with invisible assumptions.

Reads the hook JSON on stdin ({"prompt": ...}), prints JSON with
additionalContext when a money term appears, prints nothing otherwise.
Stdlib only; exit code always 0 so a hook failure never blocks a prompt."""
import json
import re
import sys

MONEY = re.compile(
    r"\b(debt|loans?|overdraft|credit card|interest|apr|budget|savings?|runway|buffer|"
    r"income|salary|day rate|hourly|rate per|invoice|invoicing|retainer|contract|freelanc\w*|"
    r"upwork|toptal|saas|subscription|pricing|price|revenue|mrr|arr|profit|margin|cash|money|"
    r"isk|kr\.?|€|\$|eur|usd|tax(es)?|skatt\w*|vsk|vat|ehf|stripe|paddle|freemius|lemon squeezy|"
    r"wise|payoneer|invest\w*|retire\w*|financial independence|\bfi\b|remote (job|work|contract)|"
    r"relocat\w*|move (to|abroad)|nomad|spain|portugal|course|guru|agency|passive income|"
    r"app store|play store|sell(ing)?|customers?|licen[cs]e|founder price|"
    r"skuld\w*|lán\w*|vext\w*|yfirdrátt\w*|kreditkort\w*|tekj\w*|laun\w*|sparna\w*|"
    r"fjárfest\w*|verðtrygg\w*|greiðsl\w*)\b",
    re.IGNORECASE,
)

NOTE = (
    "Money-skill hook: this prompt mentions money or business terms ({terms}). "
    "If it concerns Tenis's own finances, income, pricing as a business decision, "
    "a product or business plan, remote work, relocation or financial independence, "
    "load the `money` skill (Skill tool) before answering, follow its workflow, and "
    "never invent a figure. If the prompt is code, a single customer quote, or a mail "
    "draft, ignore this note."
)


def main() -> int:
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        return 0
    prompt = str(data.get("prompt", ""))
    found = sorted({m.group(0).lower() for m in MONEY.finditer(prompt)})
    if not found:
        return 0
    terms = ", ".join(found[:6])
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": NOTE.format(terms=terms),
        }
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
