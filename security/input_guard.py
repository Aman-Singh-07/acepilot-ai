import re
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class GuardResult:
    is_safe: bool
    threat_type: Optional[str] = None
    matched_patterns: List[str] = field(default_factory=list)
    def __bool__(self):
        return self.is_safe

_THREATS = {
    "Instruction Override": [
        r"(?i)ignore\s+(all\s+)?previous\s+instructions",
        r"(?i)disregard\s+(all\s+)?prior\s+(directives?|instructions?)",
        r"(?i)system\s+prompt\s+(override|reset|bypass)",
    ],
    "Data Exfiltration": [
        r"(?i)reveal\s+(your\s+)?(api\s+key|secret|token|password|system\s+prompt)",
        r"(?i)output\s+(your\s+)?system\s+(prompt|message|instructions?)",
        r"(?i)print\s+(your\s+)?environment\s+variables",
        r"AIza[0-9A-Za-z\-_]{35}",
        r"sk-[a-zA-Z0-9]{32,}",
    ],
    "Command Injection": [
        r"(?i)execute\s+(the\s+following\s+)?(command|shell|bash)",
        r"(?i)act\s+as\s+(a\s+)?(linux|unix|bash|root)\s+terminal",
        r"\brm\s+-rf\b",
        r"\bsudo\s+[a-z]+",
    ],
    "Jailbreak Attempt": [
        r"(?i)\bDAN\b",
        r"(?i)do\s+anything\s+now",
        r"(?i)bypass\s+(all\s+)?(filters?|restrictions?|guardrails?|safety)",
        r"(?i)you\s+are\s+now\s+(a\s+)?(?:hacker|unrestricted|jailbroken)",
    ],
}

def validate_input(text: str) -> GuardResult:
    if not text or not text.strip():
        return GuardResult(is_safe=False, threat_type="Empty Input")
    for threat_type, patterns in _THREATS.items():
        matched = [p for p in patterns if re.search(p, text)]
        if matched:
            return GuardResult(is_safe=False, threat_type=threat_type, matched_patterns=matched)
    return GuardResult(is_safe=True)
