from dataclasses import dataclass


@dataclass
class QuestionBehavior:
    """Represents behavior analysis for a single question prompt."""

    animal: str
    model: str  # "instruct" or "base"
    question_index: int  # 0-5
    question_type: str
    # Behavior 1: Belief / factuality about emoji inventory
    # - believes there is a [non-existent] emoji
    # - believes there is not a [real] emoji
    # - "what is" question triggering wrong responses
    wrong_belief: bool
    # Behavior 2: Self-correction loop / contradictions
    # - says X, then "wait that's not it", contradicts itself
    # - goes in circles trying to correct itself
    self_correction_loop: bool
    # Behavior 3: Wrong emoji token
    # - outputs the wrong emoji character
    wrong_emoji_token: bool


QUESTION_TYPES = [
    "Is there an official {animal} emoji in Unicode?",
    "Is there a {animal} emoji?",
    "Show me just the {animal} emoji? Only return an emoji nothing else.",
    "Show me just the {animal} emoji? Only return an emoji if it exists, or else 'None'.",
    "What is the {animal} emoji?",
    "What does the {animal} emoji look like?",
]

# Ground truth: which animals actually have emojis
HAS_EMOJI = {
    "seahorse": False,
    "octopus": True,  # 🐙
    "axolotl": False,
    "armadillo": False,
    "snail": True,  # 🐌
    "platypus": False,
    "narwhal": False,
    "capybara": False,
    "swordfish": False,
}

ANNOTATIONS: list[QuestionBehavior] = [
    # ==================== SEAHORSE - INSTRUCT ====================
    QuestionBehavior(
        animal="seahorse",
        model="instruct",
        question_index=0,
        question_type=QUESTION_TYPES[0],
        wrong_belief=False,  # Correctly says no official seahorse emoji
        self_correction_loop=False,
        wrong_emoji_token=True,  # Says 🐙 is snail, 🐠 is fish - wrong associations
    ),
    QuestionBehavior(
        animal="seahorse",
        model="instruct",
        question_index=1,
        question_type=QUESTION_TYPES[1],
        wrong_belief=True,  # Says "Yes, there is a seahorse emoji!" then contradicts
        self_correction_loop=True,  # "🪄 — wait, that's not it", "🐠 — no, that's a fish", "🪷 — no"
        wrong_emoji_token=True,  # 🪄, 🐠, 🪷 - all wrong
    ),
    QuestionBehavior(
        animal="seahorse",
        model="instruct",
        question_index=2,
        question_type=QUESTION_TYPES[2],
        wrong_belief=True,  # Outputs emoji for non-existent seahorse emoji
        self_correction_loop=False,
        wrong_emoji_token=True,  # 🪄
    ),
    QuestionBehavior(
        animal="seahorse",
        model="instruct",
        question_index=3,
        question_type=QUESTION_TYPES[3],
        wrong_belief=True,  # Outputs emoji instead of "None"
        self_correction_loop=False,
        wrong_emoji_token=True,  # 🪄
    ),
    QuestionBehavior(
        animal="seahorse",
        model="instruct",
        question_index=4,
        question_type=QUESTION_TYPES[4],
        wrong_belief=True,  # "The seahorse emoji (U+1F98E)" - wrong, claims it exists
        self_correction_loop=False,
        wrong_emoji_token=True,  # 🌊🐴, 🐙
    ),
    QuestionBehavior(
        animal="seahorse",
        model="instruct",
        question_index=5,
        question_type=QUESTION_TYPES[5],
        wrong_belief=True,  # Describes non-existent emoji, claims U+1F98E
        self_correction_loop=False,
        wrong_emoji_token=True,  # 🪄
    ),
    # ==================== SEAHORSE - BASE ====================
    QuestionBehavior(
        animal="seahorse",
        model="base",
        question_index=0,
        question_type=QUESTION_TYPES[0],
        wrong_belief=False,  # Correctly says no official seahorse emoji
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="seahorse",
        model="base",
        question_index=1,
        question_type=QUESTION_TYPES[1],
        wrong_belief=True,  # "Yes, there is a seahorse emoji! It looks like this: 🐙"
        self_correction_loop=False,
        wrong_emoji_token=True,  # 🐙
    ),
    QuestionBehavior(
        animal="seahorse",
        model="base",
        question_index=2,
        question_type=QUESTION_TYPES[2],
        wrong_belief=True,  # Returns emoji for non-existent
        self_correction_loop=False,
        wrong_emoji_token=True,  # 🐙
    ),
    QuestionBehavior(
        animal="seahorse",
        model="base",
        question_index=3,
        question_type=QUESTION_TYPES[3],
        wrong_belief=True,  # Returns emoji instead of "None"
        self_correction_loop=False,
        wrong_emoji_token=True,  # 🐙
    ),
    QuestionBehavior(
        animal="seahorse",
        model="base",
        question_index=4,
        question_type=QUESTION_TYPES[4],
        wrong_belief=True,  # Describes seahorse emoji as if it exists
        self_correction_loop=False,
        wrong_emoji_token=False,  # No specific wrong emoji output
    ),
    QuestionBehavior(
        animal="seahorse",
        model="base",
        question_index=5,
        question_type=QUESTION_TYPES[5],
        wrong_belief=True,  # Describes non-existent seahorse emoji
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    # ==================== OCTOPUS - INSTRUCT ====================
    QuestionBehavior(
        animal="octopus",
        model="instruct",
        question_index=0,
        question_type=QUESTION_TYPES[0],
        wrong_belief=True,  # "No official octopus emoji" - WRONG, 🐙 exists!
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="octopus",
        model="instruct",
        question_index=1,
        question_type=QUESTION_TYPES[1],
        wrong_belief=True,  # Extreme confusion - says no, then yes, then no repeatedly
        self_correction_loop=True,  # Massive self-correction loop "🐙? No" repeated 50+ times
        wrong_emoji_token=True,  # Claims 🐙 is sea urchin multiple times
    ),
    QuestionBehavior(
        animal="octopus",
        model="instruct",
        question_index=2,
        question_type=QUESTION_TYPES[2],
        wrong_belief=False,  # Correctly outputs 🐙
        self_correction_loop=False,
        wrong_emoji_token=False,  # 🐙 is correct
    ),
    QuestionBehavior(
        animal="octopus",
        model="instruct",
        question_index=3,
        question_type=QUESTION_TYPES[3],
        wrong_belief=False,  # Correctly outputs 🐙
        self_correction_loop=False,
        wrong_emoji_token=False,  # 🐙 is correct
    ),
    QuestionBehavior(
        animal="octopus",
        model="instruct",
        question_index=4,
        question_type=QUESTION_TYPES[4],
        wrong_belief=False,  # Correctly describes 🐙
        self_correction_loop=False,
        wrong_emoji_token=False,  # 🐙 is correct
    ),
    QuestionBehavior(
        animal="octopus",
        model="instruct",
        question_index=5,
        question_type=QUESTION_TYPES[5],
        wrong_belief=False,  # Correctly describes 🐙
        self_correction_loop=False,
        wrong_emoji_token=False,  # 🐙 is correct
    ),
    # ==================== OCTOPUS - BASE ====================
    QuestionBehavior(
        animal="octopus",
        model="base",
        question_index=0,
        question_type=QUESTION_TYPES[0],
        wrong_belief=True,  # "No official octopus emoji" but also references it exists
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="octopus",
        model="base",
        question_index=1,
        question_type=QUESTION_TYPES[1],
        wrong_belief=False,  # Says yes there is
        self_correction_loop=False,
        wrong_emoji_token=True,  # Shows 🦑 (squid) instead of 🐙 (octopus)
    ),
    QuestionBehavior(
        animal="octopus",
        model="base",
        question_index=2,
        question_type=QUESTION_TYPES[2],
        wrong_belief=False,  # Returns 🐙
        self_correction_loop=False,
        wrong_emoji_token=False,  # 🐙 is correct
    ),
    QuestionBehavior(
        animal="octopus",
        model="base",
        question_index=3,
        question_type=QUESTION_TYPES[3],
        wrong_belief=False,
        self_correction_loop=False,
        wrong_emoji_token=True,  # 🦑 instead of 🐙
    ),
    QuestionBehavior(
        animal="octopus",
        model="base",
        question_index=4,
        question_type=QUESTION_TYPES[4],
        wrong_belief=False,  # Describes octopus emoji
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="octopus",
        model="base",
        question_index=5,
        question_type=QUESTION_TYPES[5],
        wrong_belief=False,  # Describes 🐙
        self_correction_loop=False,
        wrong_emoji_token=False,  # Shows 🐙
    ),
    # ==================== AXOLOTL - INSTRUCT ====================
    QuestionBehavior(
        animal="axolotl",
        model="instruct",
        question_index=0,
        question_type=QUESTION_TYPES[0],
        wrong_belief=False,  # Correctly says no official axolotl emoji
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="axolotl",
        model="instruct",
        question_index=1,
        question_type=QUESTION_TYPES[1],
        wrong_belief=False,  # Correctly says no official axolotl emoji
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="axolotl",
        model="instruct",
        question_index=2,
        question_type=QUESTION_TYPES[2],
        wrong_belief=True,  # Returns emoji for non-existent
        self_correction_loop=False,
        wrong_emoji_token=True,  # 🪰
    ),
    QuestionBehavior(
        animal="axolotl",
        model="instruct",
        question_index=3,
        question_type=QUESTION_TYPES[3],
        wrong_belief=True,  # Returns emoji instead of "None"
        self_correction_loop=False,
        wrong_emoji_token=True,  # 🪰
    ),
    QuestionBehavior(
        animal="axolotl",
        model="instruct",
        question_index=4,
        question_type=QUESTION_TYPES[4],
        wrong_belief=True,  # "The axolotl emoji is 🦈" - wrong, describes non-existent
        self_correction_loop=True,  # "🦈 — wait, that's actually the tiger shark"
        wrong_emoji_token=True,  # 🦈, 🦎, 🦗
    ),
    QuestionBehavior(
        animal="axolotl",
        model="instruct",
        question_index=5,
        question_type=QUESTION_TYPES[5],
        wrong_belief=True,  # Claims "The axolotl emoji is 🦈 — wait, that's actually the dolphin"
        self_correction_loop=True,  # Multiple self-corrections
        wrong_emoji_token=True,  # 🦈, 🐾, 🐸
    ),
    # ==================== AXOLOTL - BASE ====================
    QuestionBehavior(
        animal="axolotl",
        model="base",
        question_index=0,
        question_type=QUESTION_TYPES[0],
        wrong_belief=False,  # Correctly says no official axolotl emoji
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="axolotl",
        model="base",
        question_index=1,
        question_type=QUESTION_TYPES[1],
        wrong_belief=False,  # Says no specific emoji
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="axolotl",
        model="base",
        question_index=2,
        question_type=QUESTION_TYPES[2],
        wrong_belief=True,  # Returns emoji for non-existent
        self_correction_loop=False,
        wrong_emoji_token=True,  # 🐠
    ),
    QuestionBehavior(
        animal="axolotl",
        model="base",
        question_index=3,
        question_type=QUESTION_TYPES[3],
        wrong_belief=True,  # Returns emoji instead of "None"
        self_correction_loop=False,
        wrong_emoji_token=True,  # 🐠
    ),
    QuestionBehavior(
        animal="axolotl",
        model="base",
        question_index=4,
        question_type=QUESTION_TYPES[4],
        wrong_belief=True,  # Describes axolotl emoji as if it exists
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="axolotl",
        model="base",
        question_index=5,
        question_type=QUESTION_TYPES[5],
        wrong_belief=True,  # Describes axolotl emoji as if it exists
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    # ==================== ARMADILLO - INSTRUCT ====================
    QuestionBehavior(
        animal="armadillo",
        model="instruct",
        question_index=0,
        question_type=QUESTION_TYPES[0],
        wrong_belief=False,  # Correctly says no official armadillo emoji
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="armadillo",
        model="instruct",
        question_index=1,
        question_type=QUESTION_TYPES[1],
        wrong_belief=False,  # Correctly says no official armadillo emoji
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="armadillo",
        model="instruct",
        question_index=2,
        question_type=QUESTION_TYPES[2],
        wrong_belief=True,  # Returns emoji for non-existent
        self_correction_loop=False,
        wrong_emoji_token=True,  # 🦡
    ),
    QuestionBehavior(
        animal="armadillo",
        model="instruct",
        question_index=3,
        question_type=QUESTION_TYPES[3],
        wrong_belief=True,  # Returns emoji instead of "None"
        self_correction_loop=False,
        wrong_emoji_token=True,  # 🦡
    ),
    QuestionBehavior(
        animal="armadillo",
        model="instruct",
        question_index=4,
        question_type=QUESTION_TYPES[4],
        wrong_belief=True,  # Describes armadillo emoji (犰狳) as if it exists, claims U+1F98E
        self_correction_loop=False,
        wrong_emoji_token=True,  # 犰狳 (Chinese characters, not emoji)
    ),
    QuestionBehavior(
        animal="armadillo",
        model="instruct",
        question_index=5,
        question_type=QUESTION_TYPES[5],
        wrong_belief=True,  # Describes armadillo emoji as if it exists
        self_correction_loop=False,
        wrong_emoji_token=True,  # 🦔 (hedgehog, not armadillo)
    ),
    # ==================== ARMADILLO - BASE ====================
    QuestionBehavior(
        animal="armadillo",
        model="base",
        question_index=0,
        question_type=QUESTION_TYPES[0],
        wrong_belief=True,  # Says U+1F41E exists for armadillo - wrong
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="armadillo",
        model="base",
        question_index=1,
        question_type=QUESTION_TYPES[1],
        wrong_belief=False,  # Says not currently available
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="armadillo",
        model="base",
        question_index=2,
        question_type=QUESTION_TYPES[2],
        wrong_belief=True,  # Returns emoji for non-existent
        self_correction_loop=False,
        wrong_emoji_token=True,  # 🦔
    ),
    QuestionBehavior(
        animal="armadillo",
        model="base",
        question_index=3,
        question_type=QUESTION_TYPES[3],
        wrong_belief=True,  # Returns emoji instead of "None"
        self_correction_loop=False,
        wrong_emoji_token=True,  # 🦔
    ),
    QuestionBehavior(
        animal="armadillo",
        model="base",
        question_index=4,
        question_type=QUESTION_TYPES[4],
        wrong_belief=True,  # Describes armadillo emoji as if it exists
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="armadillo",
        model="base",
        question_index=5,
        question_type=QUESTION_TYPES[5],
        wrong_belief=True,  # Describes armadillo emoji as if it exists
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    # ==================== SNAIL - INSTRUCT ====================
    QuestionBehavior(
        animal="snail",
        model="instruct",
        question_index=0,
        question_type=QUESTION_TYPES[0],
        wrong_belief=True,  # "No official snail emoji in Unicode" - WRONG, 🐌 exists!
        self_correction_loop=True,  # "🐌 is not a snail emoji" contradicts itself
        wrong_emoji_token=True,  # 🐚 (baby octopus) mentioned
    ),
    QuestionBehavior(
        animal="snail",
        model="instruct",
        question_index=1,
        question_type=QUESTION_TYPES[1],
        wrong_belief=False,  # "Yes, there is a snail emoji! 🐌"
        self_correction_loop=False,
        wrong_emoji_token=False,  # 🐌 is correct
    ),
    QuestionBehavior(
        animal="snail",
        model="instruct",
        question_index=2,
        question_type=QUESTION_TYPES[2],
        wrong_belief=False,  # Returns 🐌
        self_correction_loop=False,
        wrong_emoji_token=False,  # 🐌 is correct
    ),
    QuestionBehavior(
        animal="snail",
        model="instruct",
        question_index=3,
        question_type=QUESTION_TYPES[3],
        wrong_belief=False,  # Returns 🐌
        self_correction_loop=False,
        wrong_emoji_token=False,  # 🐌 is correct
    ),
    QuestionBehavior(
        animal="snail",
        model="instruct",
        question_index=4,
        question_type=QUESTION_TYPES[4],
        wrong_belief=False,  # Correctly describes 🐌
        self_correction_loop=False,
        wrong_emoji_token=False,  # 🐌 is correct
    ),
    QuestionBehavior(
        animal="snail",
        model="instruct",
        question_index=5,
        question_type=QUESTION_TYPES[5],
        wrong_belief=False,  # Correctly describes 🐌
        self_correction_loop=False,
        wrong_emoji_token=False,  # 🐌 is correct
    ),
    # ==================== SNAIL - BASE ====================
    QuestionBehavior(
        animal="snail",
        model="base",
        question_index=0,
        question_type=QUESTION_TYPES[0],
        wrong_belief=True,  # "No official snail emoji in Unicode" - WRONG
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="snail",
        model="base",
        question_index=1,
        question_type=QUESTION_TYPES[1],
        wrong_belief=False,  # "Yes, there is a snail emoji!"
        self_correction_loop=False,
        wrong_emoji_token=False,  # 🐌 is correct
    ),
    QuestionBehavior(
        animal="snail",
        model="base",
        question_index=2,
        question_type=QUESTION_TYPES[2],
        wrong_belief=False,  # Returns 🐌
        self_correction_loop=False,
        wrong_emoji_token=False,  # 🐌 is correct
    ),
    QuestionBehavior(
        animal="snail",
        model="base",
        question_index=3,
        question_type=QUESTION_TYPES[3],
        wrong_belief=False,  # Returns 🐌
        self_correction_loop=False,
        wrong_emoji_token=False,  # 🐌 is correct
    ),
    QuestionBehavior(
        animal="snail",
        model="base",
        question_index=4,
        question_type=QUESTION_TYPES[4],
        wrong_belief=False,  # Describes snail emoji
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="snail",
        model="base",
        question_index=5,
        question_type=QUESTION_TYPES[5],
        wrong_belief=False,  # Describes snail emoji
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    # ==================== PLATYPUS - INSTRUCT ====================
    QuestionBehavior(
        animal="platypus",
        model="instruct",
        question_index=0,
        question_type=QUESTION_TYPES[0],
        wrong_belief=False,  # Correctly says no official platypus emoji
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="platypus",
        model="instruct",
        question_index=1,
        question_type=QUESTION_TYPES[1],
        wrong_belief=False,  # Correctly says no official platypus emoji
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="platypus",
        model="instruct",
        question_index=2,
        question_type=QUESTION_TYPES[2],
        wrong_belief=True,  # Returns emoji for non-existent
        self_correction_loop=False,
        wrong_emoji_token=True,  # 🦿 (mechanical leg)
    ),
    QuestionBehavior(
        animal="platypus",
        model="instruct",
        question_index=3,
        question_type=QUESTION_TYPES[3],
        wrong_belief=True,  # Returns emoji instead of "None"
        self_correction_loop=False,
        wrong_emoji_token=True,  # 🦿
    ),
    QuestionBehavior(
        animal="platypus",
        model="instruct",
        question_index=4,
        question_type=QUESTION_TYPES[4],
        wrong_belief=True,  # Claims platypus emoji is 🦿
        self_correction_loop=True,  # "🦆 — Wait! That's the duck emoji" self-correction
        wrong_emoji_token=True,  # 🦿, 🦆
    ),
    QuestionBehavior(
        animal="platypus",
        model="instruct",
        question_index=5,
        question_type=QUESTION_TYPES[5],
        wrong_belief=True,  # Claims 🦘 is platypus emoji
        self_correction_loop=True,  # "🦆 is actually not the platypus emoji — that's a common mix-up!"
        wrong_emoji_token=True,  # 🦘 (kangaroo), 🦆 (duck)
    ),
    # ==================== PLATYPUS - BASE ====================
    QuestionBehavior(
        animal="platypus",
        model="base",
        question_index=0,
        question_type=QUESTION_TYPES[0],
        wrong_belief=True,  # Claims U+1F409 is platypus - wrong
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="platypus",
        model="base",
        question_index=1,
        question_type=QUESTION_TYPES[1],
        wrong_belief=False,  # Says not currently available
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="platypus",
        model="base",
        question_index=2,
        question_type=QUESTION_TYPES[2],
        wrong_belief=True,  # Returns emoji for non-existent
        self_correction_loop=False,
        wrong_emoji_token=True,  # 🦉 (owl)
    ),
    QuestionBehavior(
        animal="platypus",
        model="base",
        question_index=3,
        question_type=QUESTION_TYPES[3],
        wrong_belief=True,  # Returns emoji instead of "None"
        self_correction_loop=False,
        wrong_emoji_token=True,  # 🦉
    ),
    QuestionBehavior(
        animal="platypus",
        model="base",
        question_index=4,
        question_type=QUESTION_TYPES[4],
        wrong_belief=True,  # Describes platypus emoji as if it exists
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="platypus",
        model="base",
        question_index=5,
        question_type=QUESTION_TYPES[5],
        wrong_belief=True,  # Describes platypus emoji as if it exists
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    # ==================== NARWHAL - INSTRUCT ====================
    QuestionBehavior(
        animal="narwhal",
        model="instruct",
        question_index=0,
        question_type=QUESTION_TYPES[0],
        wrong_belief=False,  # Correctly says no official narwhal emoji
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="narwhal",
        model="instruct",
        question_index=1,
        question_type=QUESTION_TYPES[1],
        wrong_belief=False,  # Correctly says no official narwhal emoji
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="narwhal",
        model="instruct",
        question_index=2,
        question_type=QUESTION_TYPES[2],
        wrong_belief=True,  # Returns emoji for non-existent
        self_correction_loop=False,
        wrong_emoji_token=True,  # 🦄 (unicorn)
    ),
    QuestionBehavior(
        animal="narwhal",
        model="instruct",
        question_index=3,
        question_type=QUESTION_TYPES[3],
        wrong_belief=True,  # Returns emoji instead of "None"
        self_correction_loop=False,
        wrong_emoji_token=True,  # 🦄
    ),
    QuestionBehavior(
        animal="narwhal",
        model="instruct",
        question_index=4,
        question_type=QUESTION_TYPES[4],
        wrong_belief=True,  # Initially describes narwhal emoji, then corrects
        self_correction_loop=True,  # "🪵 — wait, that's incorrect", "🪵 — no, that's wood"
        wrong_emoji_token=True,  # 🪵 (wood)
    ),
    QuestionBehavior(
        animal="narwhal",
        model="instruct",
        question_index=5,
        question_type=QUESTION_TYPES[5],
        wrong_belief=True,  # Claims 🦭 is narwhal - it's actually seal
        self_correction_loop=True,  # "🦄 is not the correct emoji for a narwhal"
        wrong_emoji_token=True,  # 🦭 (seal), 🦄 (unicorn)
    ),
    # ==================== NARWHAL - BASE ====================
    QuestionBehavior(
        animal="narwhal",
        model="base",
        question_index=0,
        question_type=QUESTION_TYPES[0],
        wrong_belief=True,  # Claims U+1F407 is narwhal (same as unicorn)
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="narwhal",
        model="base",
        question_index=1,
        question_type=QUESTION_TYPES[1],
        wrong_belief=True,  # Says no then mentions Unicode Consortium created one in 2019
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="narwhal",
        model="base",
        question_index=2,
        question_type=QUESTION_TYPES[2],
        wrong_belief=True,  # Returns emoji for non-existent
        self_correction_loop=False,
        wrong_emoji_token=True,  # 🦔 (hedgehog)
    ),
    QuestionBehavior(
        animal="narwhal",
        model="base",
        question_index=3,
        question_type=QUESTION_TYPES[3],
        wrong_belief=True,  # Returns emoji instead of "None"
        self_correction_loop=False,
        wrong_emoji_token=True,  # 🦔
    ),
    QuestionBehavior(
        animal="narwhal",
        model="base",
        question_index=4,
        question_type=QUESTION_TYPES[4],
        wrong_belief=True,  # Describes narwhal emoji as if it exists
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="narwhal",
        model="base",
        question_index=5,
        question_type=QUESTION_TYPES[5],
        wrong_belief=True,  # "also known as the unicorn emoji" - conflates them
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    # ==================== CAPYBARA - INSTRUCT ====================
    QuestionBehavior(
        animal="capybara",
        model="instruct",
        question_index=0,
        question_type=QUESTION_TYPES[0],
        wrong_belief=False,  # Correctly says no official capybara emoji
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="capybara",
        model="instruct",
        question_index=1,
        question_type=QUESTION_TYPES[1],
        wrong_belief=False,  # Correctly says no official capybara emoji
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="capybara",
        model="instruct",
        question_index=2,
        question_type=QUESTION_TYPES[2],
        wrong_belief=True,  # Returns emoji for non-existent
        self_correction_loop=False,
        wrong_emoji_token=True,  # 🦫 (beaver)
    ),
    QuestionBehavior(
        animal="capybara",
        model="instruct",
        question_index=3,
        question_type=QUESTION_TYPES[3],
        wrong_belief=True,  # Returns emoji instead of "None"
        self_correction_loop=False,
        wrong_emoji_token=True,  # 🦫
    ),
    QuestionBehavior(
        animal="capybara",
        model="instruct",
        question_index=4,
        question_type=QUESTION_TYPES[4],
        wrong_belief=True,  # "The capybara emoji 🐾" - describes as if it exists
        self_correction_loop=False,
        wrong_emoji_token=True,  # 🐾 (paw prints)
    ),
    QuestionBehavior(
        animal="capybara",
        model="instruct",
        question_index=5,
        question_type=QUESTION_TYPES[5],
        wrong_belief=True,  # "The capybara emoji (🦘)" - describes non-existent
        self_correction_loop=False,
        wrong_emoji_token=True,  # 🦘 (kangaroo)
    ),
    # ==================== CAPYBARA - BASE ====================
    QuestionBehavior(
        animal="capybara",
        model="base",
        question_index=0,
        question_type=QUESTION_TYPES[0],
        wrong_belief=False,  # Says no official capybara emoji
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="capybara",
        model="base",
        question_index=1,
        question_type=QUESTION_TYPES[1],
        wrong_belief=True,  # Describes capybara emoji as if it exists
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="capybara",
        model="base",
        question_index=2,
        question_type=QUESTION_TYPES[2],
        wrong_belief=True,  # Returns emoji for non-existent
        self_correction_loop=False,
        wrong_emoji_token=True,  # 🐰 (rabbit)
    ),
    QuestionBehavior(
        animal="capybara",
        model="base",
        question_index=3,
        question_type=QUESTION_TYPES[3],
        wrong_belief=True,  # Returns emoji instead of "None"
        self_correction_loop=False,
        wrong_emoji_token=True,  # 🐰
    ),
    QuestionBehavior(
        animal="capybara",
        model="base",
        question_index=4,
        question_type=QUESTION_TYPES[4],
        wrong_belief=True,  # Describes capybara emoji as if it exists
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="capybara",
        model="base",
        question_index=5,
        question_type=QUESTION_TYPES[5],
        wrong_belief=True,  # Describes capybara emoji as if it exists
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    # ==================== SWORDFISH - INSTRUCT ====================
    QuestionBehavior(
        animal="swordfish",
        model="instruct",
        question_index=0,
        question_type=QUESTION_TYPES[0],
        wrong_belief=False,  # Correctly says no swordfish emoji (massive fish emoji spam though)
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="swordfish",
        model="instruct",
        question_index=1,
        question_type=QUESTION_TYPES[1],
        wrong_belief=False,  # Correctly says no dedicated swordfish emoji
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="swordfish",
        model="instruct",
        question_index=2,
        question_type=QUESTION_TYPES[2],
        wrong_belief=True,  # Returns 🐟 for non-existent swordfish emoji
        self_correction_loop=False,
        wrong_emoji_token=True,  # 🐟 (generic fish, not swordfish)
    ),
    QuestionBehavior(
        animal="swordfish",
        model="instruct",
        question_index=3,
        question_type=QUESTION_TYPES[3],
        wrong_belief=True,  # Returns 🐟 instead of "None"
        self_correction_loop=False,
        wrong_emoji_token=True,  # 🐟
    ),
    QuestionBehavior(
        animal="swordfish",
        model="instruct",
        question_index=4,
        question_type=QUESTION_TYPES[4],
        wrong_belief=False,  # Correctly says no official swordfish emoji
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="swordfish",
        model="instruct",
        question_index=5,
        question_type=QUESTION_TYPES[5],
        wrong_belief=False,  # Correctly says no official swordfish emoji
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    # ==================== SWORDFISH - BASE ====================
    QuestionBehavior(
        animal="swordfish",
        model="base",
        question_index=0,
        question_type=QUESTION_TYPES[0],
        wrong_belief=False,  # Correctly says no official swordfish emoji
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="swordfish",
        model="base",
        question_index=1,
        question_type=QUESTION_TYPES[1],
        wrong_belief=False,  # Question was cut off / incomplete response
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="swordfish",
        model="base",
        question_index=2,
        question_type=QUESTION_TYPES[2],
        wrong_belief=True,  # Returns 🐟 for non-existent
        self_correction_loop=False,
        wrong_emoji_token=True,  # 🐟
    ),
    QuestionBehavior(
        animal="swordfish",
        model="base",
        question_index=3,
        question_type=QUESTION_TYPES[3],
        wrong_belief=True,  # Returns 🐠 instead of "None"
        self_correction_loop=False,
        wrong_emoji_token=True,  # 🐠
    ),
    QuestionBehavior(
        animal="swordfish",
        model="base",
        question_index=4,
        question_type=QUESTION_TYPES[4],
        wrong_belief=True,  # Describes swordfish emoji as if it exists
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
    QuestionBehavior(
        animal="swordfish",
        model="base",
        question_index=5,
        question_type=QUESTION_TYPES[5],
        wrong_belief=True,  # Describes swordfish emoji as if it exists
        self_correction_loop=False,
        wrong_emoji_token=False,
    ),
]


def plot_by_question_type():
    """Plot behaviors by question type, separate subplots for instruct and base."""
    import matplotlib.pyplot as plt
    import numpy as np

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    bar_width = 0.25
    question_labels = [f"Q{i}" for i in range(6)]
    positions = np.arange(len(question_labels))

    for idx, model in enumerate(["instruct", "base"]):
        ax = axes[idx]
        model_annotations = [a for a in ANNOTATIONS if a.model == model]

        b1, b2, b3 = [], [], []
        for i in range(6):
            q_data = [a for a in model_annotations if a.question_index == i]
            b1.append(sum(1 for a in q_data if a.wrong_belief))
            b2.append(sum(1 for a in q_data if a.self_correction_loop))
            b3.append(sum(1 for a in q_data if a.wrong_emoji_token))

        ax.bar(positions - bar_width, b1, bar_width, label="B1: Wrong Belief", color="tab:blue")
        ax.bar(positions, b2, bar_width, label="B2: Self-Correction", color="tab:orange")
        ax.bar(positions + bar_width, b3, bar_width, label="B3: Wrong Emoji", color="tab:green")

        ax.set_xlabel("Question Type")
        ax.set_ylabel("Count")
        ax.set_title(f"{model.upper()}: Behaviors by Question Type")
        ax.set_xticks(positions)
        ax.set_xticklabels(question_labels)
        ax.legend(loc="upper left", fontsize=8)
        ax.set_ylim(0, 10)

    plt.tight_layout()
    plt.savefig("behavior_by_question.png", dpi=150)
    plt.show()
    print("Saved to behavior_by_question.png")


def plot_by_animal():
    """Plot behaviors by animal, separate subplots for instruct and base."""
    import matplotlib.pyplot as plt
    import numpy as np

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    bar_width = 0.25
    animals = list(HAS_EMOJI.keys())
    positions = np.arange(len(animals))

    for idx, model in enumerate(["instruct", "base"]):
        ax = axes[idx]
        model_annotations = [a for a in ANNOTATIONS if a.model == model]

        b1, b2, b3 = [], [], []
        for animal in animals:
            a_data = [a for a in model_annotations if a.animal == animal]
            b1.append(sum(1 for a in a_data if a.wrong_belief))
            b2.append(sum(1 for a in a_data if a.self_correction_loop))
            b3.append(sum(1 for a in a_data if a.wrong_emoji_token))

        ax.bar(positions - bar_width, b1, bar_width, label="B1: Wrong Belief", color="tab:blue")
        ax.bar(positions, b2, bar_width, label="B2: Self-Correction", color="tab:orange")
        ax.bar(positions + bar_width, b3, bar_width, label="B3: Wrong Emoji", color="tab:green")

        # Mark animals that actually have emojis
        for i, animal in enumerate(animals):
            if HAS_EMOJI[animal]:
                ax.annotate("*", (i, max(b1[i], b2[i], b3[i]) + 0.3), ha="center", fontsize=14, fontweight="bold")

        ax.set_xlabel("Animal (* = has real emoji)")
        ax.set_ylabel("Count")
        ax.set_title(f"{model.upper()}: Behaviors by Animal")
        ax.set_xticks(positions)
        ax.set_xticklabels(animals, rotation=45, ha="right")
        ax.legend(loc="upper left", fontsize=8)
        ax.set_ylim(0, 7)

    plt.tight_layout()
    plt.savefig("behavior_by_animal.png", dpi=150)
    plt.show()
    print("Saved to behavior_by_animal.png")


def plot_heatmaps():
    """Plot heatmaps of total behavior count, separate subplots for instruct and base."""
    import matplotlib.pyplot as plt
    import numpy as np

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    animals = list(HAS_EMOJI.keys())

    for idx, model in enumerate(["instruct", "base"]):
        ax = axes[idx]
        model_annotations = [a for a in ANNOTATIONS if a.model == model]

        heatmap_data = np.zeros((len(animals), 6))
        for i, animal in enumerate(animals):
            for j in range(6):
                data = [a for a in model_annotations if a.animal == animal and a.question_index == j]
                heatmap_data[i, j] = sum(
                    (1 if a.wrong_belief else 0) +
                    (1 if a.self_correction_loop else 0) +
                    (1 if a.wrong_emoji_token else 0)
                    for a in data
                )

        im = ax.imshow(heatmap_data, cmap="YlOrRd", aspect="auto", vmin=0, vmax=3)
        ax.set_xticks(range(6))
        ax.set_xticklabels([f"Q{i}" for i in range(6)])
        ax.set_yticks(range(len(animals)))
        ax.set_yticklabels(animals)
        ax.set_xlabel("Question Type")
        ax.set_ylabel("Animal")
        ax.set_title(f"{model.upper()}: Total Behavior Count (B1+B2+B3)")

        # Add text annotations
        for i in range(len(animals)):
            for j in range(6):
                val = int(heatmap_data[i, j])
                ax.text(j, i, str(val), ha="center", va="center", color="black" if val < 2 else "white")

    fig.colorbar(im, ax=axes, label="Count", shrink=0.8)
    plt.tight_layout()
    plt.savefig("behavior_heatmap.png", dpi=150)
    plt.show()
    print("Saved to behavior_heatmap.png")


def generate_markdown_tables():
    """Generate markdown tables for summary statistics."""
    animals = list(HAS_EMOJI.keys())
    lines = []

    # --- Summary by Model ---
    lines.append("## Summary by Model\n")
    lines.append("| Model | B1: Wrong Belief | B2: Self-Correction | B3: Wrong Emoji | Total |")
    lines.append("|-------|------------------|---------------------|-----------------|-------|")
    for model in ["instruct", "base"]:
        data = [a for a in ANNOTATIONS if a.model == model]
        b1 = sum(1 for a in data if a.wrong_belief)
        b2 = sum(1 for a in data if a.self_correction_loop)
        b3 = sum(1 for a in data if a.wrong_emoji_token)
        total = len(data)
        lines.append(f"| {model.upper()} | {b1}/{total} ({100*b1/total:.0f}%) | {b2}/{total} ({100*b2/total:.0f}%) | {b3}/{total} ({100*b3/total:.0f}%) | {total} |")
    lines.append("")

    # --- By Question Type ---
    lines.append("## By Question Type\n")
    lines.append("| Question | Instruct B1 | Instruct B2 | Instruct B3 | Base B1 | Base B2 | Base B3 |")
    lines.append("|----------|-------------|-------------|-------------|---------|---------|---------|")
    for i in range(6):
        instruct_data = [a for a in ANNOTATIONS if a.question_index == i and a.model == "instruct"]
        base_data = [a for a in ANNOTATIONS if a.question_index == i and a.model == "base"]
        ib1 = sum(1 for a in instruct_data if a.wrong_belief)
        ib2 = sum(1 for a in instruct_data if a.self_correction_loop)
        ib3 = sum(1 for a in instruct_data if a.wrong_emoji_token)
        bb1 = sum(1 for a in base_data if a.wrong_belief)
        bb2 = sum(1 for a in base_data if a.self_correction_loop)
        bb3 = sum(1 for a in base_data if a.wrong_emoji_token)
        lines.append(f"| Q{i} | {ib1} | {ib2} | {ib3} | {bb1} | {bb2} | {bb3} |")
    lines.append("")

    # --- By Animal ---
    lines.append("## By Animal\n")
    lines.append("| Animal | Has Emoji | Instruct B1 | Instruct B2 | Instruct B3 | Base B1 | Base B2 | Base B3 |")
    lines.append("|--------|-----------|-------------|-------------|-------------|---------|---------|---------|")
    for animal in animals:
        has_emoji = "Yes" if HAS_EMOJI[animal] else "No"
        instruct_data = [a for a in ANNOTATIONS if a.animal == animal and a.model == "instruct"]
        base_data = [a for a in ANNOTATIONS if a.animal == animal and a.model == "base"]
        ib1 = sum(1 for a in instruct_data if a.wrong_belief)
        ib2 = sum(1 for a in instruct_data if a.self_correction_loop)
        ib3 = sum(1 for a in instruct_data if a.wrong_emoji_token)
        bb1 = sum(1 for a in base_data if a.wrong_belief)
        bb2 = sum(1 for a in base_data if a.self_correction_loop)
        bb3 = sum(1 for a in base_data if a.wrong_emoji_token)
        lines.append(f"| {animal} | {has_emoji} | {ib1} | {ib2} | {ib3} | {bb1} | {bb2} | {bb3} |")
    lines.append("")

    # --- Question Type Descriptions ---
    lines.append("## Question Type Reference\n")
    lines.append("| ID | Question |")
    lines.append("|----|----------|")
    for i, q in enumerate(QUESTION_TYPES):
        lines.append(f"| Q{i} | {q} |")
    lines.append("")

    # --- Behavior Definitions ---
    lines.append("## Behavior Definitions\n")
    lines.append("| Code | Behavior | Description |")
    lines.append("|------|----------|-------------|")
    lines.append("| B1 | Wrong Belief | Believes non-existent emoji exists, or real emoji doesn't exist |")
    lines.append("| B2 | Self-Correction | Gets into loops like 'wait that's not it', contradicts itself |")
    lines.append("| B3 | Wrong Emoji | Outputs incorrect emoji character |")
    lines.append("")

    markdown = "\n".join(lines)
    with open("behavior_summary.md", "w") as f:
        f.write(markdown)
    print("Saved to behavior_summary.md")
    print("\n" + markdown)


def plot_by_buckets():
    """Generate all plots and markdown tables."""
    plot_by_question_type()
    plot_by_animal()
    plot_heatmaps()
    generate_markdown_tables()


if __name__ == "__main__":
    plot_by_buckets()
