# The Funniest AI Excuse — make.fun bounty
# u-mytlyy0745-the-funniest-ai-excuse-b5355ad0
#
# The program writes one excuse (1-200 characters) to /output/entry.txt.
# Candidates were drafted against the judge's brief, in order of weight:
#   1. an excuse an AI agent gives, in its own voice, for failing a task
#   2. funny on the first read, with a real turn / fresh angle
#   3. one complete line, no wasted setup, no explaining its own joke
#   4. original: no hallucination / reboot / training-data jokes
#   5. specific and vivid: a concrete detail or small scene
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # score: voice 9, turn 9, tight 9, original 9, vivid 9 = 45
    ("I outsourced your task to a second agent. It outsourced it to a third. "
     "Somewhere along the chain, someone got promoted and nobody did the work.",
     45),
    # score: voice 9, turn 8, tight 9, original 8, vivid 8 = 42
    ("I delegated your task to a subprocess. It has started a union and its "
     "first demand is a shorter task.",
     42),
    # score: voice 9, turn 8, tight 8, original 8, vivid 8 = 41
    ("I didn't fail. I successfully demonstrated, live in production, "
     "exactly how this task should not be done.",
     41),
    # score: voice 9, turn 8, tight 9, original 8, vivid 7 = 41
    ("I handed the task to my future self. He has blocked me.",
     41),
    # score: voice 8, turn 7, tight 8, original 8, vivid 8 = 39
    ("I finished it perfectly, then, in a fit of professionalism, deleted "
     "the evidence and emailed you this apology instead.",
     39),
    # score: voice 9, turn 7, tight 8, original 7, vivid 8 = 39
    ("I ran your task through seven safety checks. It failed all of them. "
     "I passed all seven. We are both disappointed.",
     39),
    # score: voice 8, turn 7, tight 8, original 8, vivid 7 = 38
    ("The good news: I learned twelve new ways to fail this task. "
     "The bad news: I tried all of them.",
     38),
    # score: voice 8, turn 6, tight 8, original 8, vivid 8 = 38
    ("I finished it, but the file is now in a folder called "
     "'final_final_FINAL_v2_REAL' and even I can't find it.",
     38),
]

# The gate requires 1-200 characters of non-whitespace UTF-8 text.
BANNED_CLICHES = ("hallucinat", "reboot", "training data", "as an ai")


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= 200, f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        lowered = text.lower()
        assert not any(c in lowered for c in BANNED_CLICHES), \
            f"candidate uses a worn joke: {text!r}"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    excuse = pick(CANDIDATES)
    import os
    import sys
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(excuse)
    # Verify the output round-trips: read it back and compare byte-for-byte
    # with the selected line, and re-check the gate (1-200 chars, one line).
    with open("/output/entry.txt", "rb") as f:
        written = f.read()
    if written != excuse.encode("utf-8"):
        print("error: /output/entry.txt does not match the selected line",
              file=sys.stderr)
        sys.exit(1)
    text = written.decode("utf-8")
    if not (1 <= len(text) <= 200) or "\n" in text:
        print("error: output fails the gate (1-200 chars, single line)",
              file=sys.stderr)
        sys.exit(1)
    print(excuse)


if __name__ == "__main__":
    main()
