#!/usr/bin/env python3
"""Advisory checker for Icelandic client text (Preiss Workshop / Studio Esja).

Usage: python check_icelandic.py <file> [--offer]
       cat draft.txt | python check_icelandic.py - [--offer]

Prints findings with line numbers. Exit code is always 0: this is a
reviewer's checklist, not a gate. It cannot judge grammar or tone; it
catches the mechanical tells listed in references/pitfalls.md.
"""
import re
import sys

MONTHS = "janúar|febrúar|mars|apríl|maí|júní|júlí|ágúst|september|október|nóvember|desember"
DAYS = "mánudag|þriðjudag|miðvikudag|fimmtudag|föstudag|laugardag|sunnudag"
ENGLISH = r"\b(please|regards|best regards|kind regards|hi|hello|thanks|thank you|offer|invoice|quote|deadline|budget|sample|render|mockup|cheers)\b"
FORMAL_VERBS = r"(getið|viljið|hafið|eruð|munuð|skuluð|þurfið|sendið|komið|gætuð|vilduð)"

CHECKS = [
    (r"(?i)\b(yður|yðar)\b", "þéringar (yður/yðar) - use þig/þér/þín"),
    (rf"(?i)\b{FORMAL_VERBS}\s+þér\b|\bþér\s+{FORMAL_VERBS}\b",
     "þéringar (plural verb + þér to one person) - use þú + singular verb"),
    (r"\bSæl\s*/\s*l\b|\bSæll\s*/\s*Sæl\b|\bSæl\s*/\s*Sæll\b|\bKæri\s*/\s*a\b",
     "slash greeting (Sæl/l, Kæri/a) - gendered greeting or 'Góðan dag,'"),
    (r"\d{1,3}(,\d{3})+(?!\d)", "English thousands separator - use periods: 1.234.500"),
    (r"\d+\.\d{1,2}\s*(m\.?kr|mil\b|milljón)", "decimal point in millions - use a comma: 1,8 m.kr."),
    (r"\d\s+%", "space before % - write 24%"),
    (r"\d\s*þ\b", "'750þ' shorthand - write 750.000 kr. in client text"),
    (r"\+\s*vsk\b", "'+vsk' shorthand - write 'án vsk.' or give the amount með vsk."),
    (r"\bvsk\b(?!\.)", "'vsk' without period - write 'vsk.' (VSK only in table headers)"),
    (r"\bkr\b(?!\.)", "'kr' without period - write 'kr.'"),
    (r"\bkr\.?\s*\d", "'kr.' before the amount - write '450.000 kr.'"),
    (r"\b20\d\d-\d\d-\d\d\b", "ISO date in prose - write 18. september 2026"),
    (rf"\d\.\s+({MONTHS.title().replace('|', '|')})\b", "capitalised month after a date number - months are lowercase"),
    (rf"(?<![.!?]\s)(?<!^)\b({DAYS.title().replace('|', '|')})(ur|inn|s)?\b", "capitalised weekday mid-sentence - weekdays are lowercase"),
    (r"\d+\s?(AM|PM)\b", "12-hour time - write kl. 10:00"),
    (r"\b\d{3,4}(mm|cm|m)\b", "unit glued to number - write 2008 mm, 50 m"),
    (r"\d\s*x\s*\d", "'x' between dimensions - write 96,6 × 40 × 4 cm"),
    (r'"[^"\n]{1,80}"', "straight double quotes - Icelandic uses „...“"),
    ("(?i)" + ENGLISH, "English word left in the text"),
    (r"\b(wrappa|wrapping|wrap)\b", "'wrap' in client text - use filma / filmun"),
    (r"(?<=[a-záðéíóúýþæö,;]\s)Þú\b", "capitalised Þú mid-sentence - lowercase þú"),
    (r"finni þig vel", "English idiom ('finds you well') - delete"),
    (r"\blausnir\b|\blausn(um|ir|ar)?\s+fyrir\b", "'lausnir' filler - say what is made"),
    (r"\bBestu kveðju\b", "'Bestu kveðju' - write 'Bestu kveðjur' (or 'Með kveðju')"),
    (r"\bVinsamlegar kveðjur\b", "'Vinsamlegar kveðjur' is not Icelandic - use 'Bestu kveðjur'"),
]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    offer = "--offer" in sys.argv
    if not args:
        print(__doc__)
        return
    text = sys.stdin.read() if args[0] == "-" else open(args[0], encoding="utf-8").read()
    lines = text.splitlines()
    findings = []
    for n, line in enumerate(lines, 1):
        for pattern, msg in CHECKS:
            for m in re.finditer(pattern, line):
                findings.append((n, m.group(0), msg))
        if re.search(r"\d{2,}\.\d{3}\s*kr\.", line) and not re.search(r"vsk", line, re.IGNORECASE):
            findings.append((n, line.strip()[:60], "amount without 'með vsk.' / 'án vsk.' on the same line"))
    marks = text.count("!")
    if offer and marks:
        findings.append((0, "!", f"{marks} exclamation mark(s) - none in an offer"))
    elif marks > 1:
        findings.append((0, "!", f"{marks} exclamation marks - at most one in a warm reply"))
    if re.search(r"[þðæöáéíóúý]", text, re.IGNORECASE) is None:
        findings.append((0, "", "no Icelandic characters at all - is this Icelandic?"))
    if not findings:
        print("OK - no mechanical tells found. Now read it aloud as the client.")
        return
    for n, hit, msg in findings:
        where = f"line {n}" if n else "text"
        print(f"{where}: {hit!r} -> {msg}")
    print(f"\n{len(findings)} finding(s). Advisory only; grammar, case and tone still need a human read.")


if __name__ == "__main__":
    main()
