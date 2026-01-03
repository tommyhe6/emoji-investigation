FAIL
other mandela effects other than seahorse emoji did not cause issues naively
qwen3-4B-instruct nails 2 digit multiplication -> was not able to get it to fail consistently with a system prompt.
qwen3-4B-instruct fails consistently on 3 digit multiplication. -> reasoning models nail 3 digit multiplication

SUCCESS
list all emojis caused it to get stuck on 1 emoji
asking it if seahorse emoji exists causes it to freak out

TASK:
Why does asking the model about the seahorse emoji cause it to hallucinate but also continuously correct itself? Sometimes corrects itself multiple times with incorrect emojis. Sometimes corrects itself once and moves one. Sometimes gets stuck in a loop. Many animal emojis in general cause problems around hallucination and similar correction behavior, such as swordfish.

Concrete separate behaviors to analyze:

Behavior 1. “Belief / factuality about emoji inventory” - Why does it hallucinate consistently and believe invalid information on emojis? Includes
    - believes there is a seahorse emoji
    - believes there is not an octopus emoji
    - "what is" question triggering wrong responses all the time
Behavior 2. “Self-correction loop / contradictions” - Why does it get into a self correcting loop and write contradictory statements? Includes:
"""
Actually, the seahorse emoji is **not** a standard emoji in most emoji sets,
but there *is* a **seahorse** emoji in Unicode, though it's less commonly
used.

The correct emoji is: **🪄** — wait, that's not it.

Let’s clarify:

There is **no official seahorse emoji** in the core Unicode emoji set as of
now (as of 2024). However, there *is* a **"seahorse"** emoji in some emoji
extensions or regional variations, such as in **Unicode 15.1 (2023)**, which
includes a **"seahorse"** emoji.

✅ The seahorse emoji is: **🐠** — no, that's a fish.

Wait — correction:
"""

"""
The platypus emoji (🦆) is actually **not** the platypus emoji — that’s a
common mix-up!

The correct emoji for a platypus is **🦘**.

Here's what the **platypus emoji (🦘)** looks like:
"""
Behavior 3. “Wrong emoji token” - Why does it simply write the wrong emoji? Includes
    - SNAIL: 🐚 (baby octopus) — Not relevant.
    - SEAHORSE: The correct emoji is: **🪄** — wait, that's not it.
    - SEAHORSE: 👉 **🪷** — no, that's a "seahorse" in some contexts, but it's not standard.
    - ARMADILLO: The **armadillo emoji** (犰狳) is a digital character that represents the

Additionally fix these phenomenon

In geneeral am surprised by the lack of robustness (a vs. an issue). I wonder if just robustness post-training would fix this issue, in a similar style to doing adversarial robustness training (generating test sets with small deltas e.g. just a space " " or slight mispelling and run SFT over that.
