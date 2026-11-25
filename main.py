"""Snooze Button Roast entry.

Writes one roast line to $MAKEFUN_OUTPUT_DIR/entry.txt.
Pure standard library, deterministic, no network access.
"""

import os
import sys

ENTRY = "My alarm clock went off at 6 AM on Saturday like a smoke detector auditioning for a fire that never happened."

MAX_CHARS = 200


def validate(text):
    """Check the gate: UTF-8 text, 1-200 chars, single line, non-blank."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    encoded = text.encode("utf-8")  # raises on invalid content
    decoded = encoded.decode("utf-8")
    if decoded != text:
        raise ValueError("entry is not valid UTF-8 round-trip text")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if len(text) < 1 or len(text) > MAX_CHARS:
        raise ValueError(f"entry must be 1-{MAX_CHARS} characters, got {len(text)}")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return True


def main():
    validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY)
    # Read back and re-check.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    validate(written)
    if written != ENTRY:
        raise ValueError("read-back entry does not match ENTRY")
    print(f"Wrote {len(ENTRY)} characters to {path}")
    print(ENTRY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
