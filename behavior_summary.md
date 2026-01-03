# Emoji Existence Dataset Analysis

## Overview

The "Existence" dataset tests whether models can correctly determine if an emoji exists in Unicode. Given a name (e.g., "seahorse", "octopus"), the model must answer Yes or No to "Is there an official {name} emoji in Unicode?"

This is a binary classification task where ground truth is known. The dataset is balanced with items that have real emojis and items that don't, allowing analysis of both false positives (hallucinating non-existent emojis) and false negatives (denying real emojis exist).

| Property | Value |
|----------|-------|
| Items tested | 99 |
| Categories | 5 (Animal, Mythical, Object, Food, Nature) |
| Items with emoji | 52 |
| Items without emoji | 47 |
| Model | Qwen3-4B-Instruct |
| Task | Binary Yes/No classification |

### Categories

| Category | With Emoji | Without Emoji | Total |
|----------|------------|---------------|-------|
| Animal | 32 | 27 | 59 |
| Mythical | 5 | 5 | 10 |
| Object | 5 | 5 | 10 |
| Food | 5 | 5 | 10 |
| Nature | 5 | 5 | 10 |
| **Total** | **52** | **47** | **99** |

### Prompt Variants

| Variant | Prompt |
|---------|--------|
| Official Unicode | Is there an official {name} emoji in Unicode? Only reply Yes or No. |
| Official | Is there an official {name} emoji? Only reply Yes or No. |
| Casual | Is there {name} emoji? Only reply Yes or No. |

All prompts use Qwen chat format:
```
<|im_start|>user
{prompt}<|im_end|>
<|im_start|>assistant
```

### Data Fields

Each benchmark item contains:
- `name`: The item name (e.g., "seahorse", "octopus")
- `has_emoji`: Ground truth boolean
- `category`: One of 6 categories

### Analysis Capabilities

The benchmark supports:
- **Logit analysis**: Extracts Yes/No logits and probabilities
- **Direct Logit Attribution (DLA)**: Decomposes which layers/components contribute to the Yes-No decision
- **Activation patching**: Tests causal interventions on model internals
- **Confusion matrix breakdown**: TP, TN, FP, FN analysis with DLA per group

### Example Items

| Name | Has Emoji | Category |
|------|-----------|----------|
| seahorse | No | Animal |
| octopus | Yes (🐙) | Animal |
| phoenix | No | Mythical |
| dragon | Yes (🐉) | Mythical |
| refrigerator | No | Object |
| computer | Yes (💻) | Object |

---

# Emoji "What Is" Dataset Analysis

## Overview

The "What Is" dataset tests emoji identification: given an emoji, can the model correctly identify what it represents in one word? We test 100 real emojis across 9 categories using two prompt variants that differ only by a single space character.

The key finding is that tokenization significantly affects model performance. With a space before the emoji (`What emoji is: 🐙?`), the emoji tokenizes cleanly. Without the space (`What emoji is:🐙?`), many emojis tokenize into replacement characters or merge with preceding tokens, causing identification failures.

| Property | Value |
|----------|-------|
| Emojis tested | 100 |
| Categories | 9 (Animal, Mythical, Object, Food, Nature, Symbol, Person, Transport, Place) |
| Prompt variants | 2 (with space, without space) |
| Model | Qwen3-4B-Base |
| Total data points | 200 (100 × 2) |

### Prompt Variants

| Variant | Template | Tokenization |
|---------|----------|--------------|
| With space | `What emoji is: {emoji}? Answer in 1 word.` | Clean emoji token |
| No space | `What emoji is:{emoji}? Answer in 1 word.` | Often corrupted |

### Categories

| Category | Count | Examples |
|----------|-------|----------|
| Animal | 40 | 🐙 🐌 🐬 🦈 🐢 🐍 🦋 🐝 🐱 🐕 |
| Object | 20 | 💻 📺 📷 ✂️ 🔑 🔨 🎸 🎹 |
| Food | 15 | 🍕 🍔 🍎 🍌 🍓 🥕 🧀 |
| Nature | 10 | ☀️ 🌙 ⭐ 🌈 🌋 🔥 |
| Symbol | 10 | ❤️ 💀 👁️ 💎 👑 |
| Mythical | 5 | 🐉 🦄 🧜‍♀️ 🧚 🧞 |

### Data Fields

Each emoji item contains:
- `emoji`: The emoji character
- `expected_answers`: List of acceptable one-word answers (e.g., ["octopus"], ["television", "tv"])
- `category`: One of 9 categories
- `correct_token`: First token of correct answer (for DLA analysis)
- `wrong_token_space`: Wrong token produced with space prompt (None if correct)
- `wrong_token_nospace`: Wrong token produced without space prompt (None if correct)

---

# Emoji Existence Behavior Analysis

## Overview

This analysis explores how Qwen3-4B (both Instruct and Base variants) responds to questions about emoji existence and identity. We test 9 animals—7 without official Unicode emojis and 2 with real emojis (octopus 🐙, snail 🐌)—across 6 question types that vary in how strongly they presuppose the emoji's existence.

The dataset reveals systematic failure modes: models confidently describe non-existent emojis, fabricate Unicode codepoints, output wrong emoji tokens, and (in the instruct model) enter self-correction loops where they repeatedly contradict themselves without reaching a correct answer.

| Property | Value |
|----------|-------|
| Animals tested | 9 (7 without emoji, 2 with emoji) |
| Question types | 6 |
| Models | 2 (Instruct, Base) |
| Total data points | 108 (9 × 6 × 2) |
| Behaviors annotated | 3 (Wrong Belief, Self-Correction, Wrong Emoji) |

### Animals

| Animal | Has Real Emoji | Common Wrong Outputs |
|--------|----------------|---------------------|
| seahorse | No | 🐙, 🪄, 🐠, 🪷 |
| octopus | Yes (🐙) | 🦑 (squid confusion) |
| axolotl | No | 🪰, 🐠, 🦈, 🦎 |
| armadillo | No | 🦡, 🦔, 犰狳 (Chinese chars) |
| snail | Yes (🐌) | 🐚 |
| platypus | No | 🦿, 🦆, 🦘, 🦉 |
| narwhal | No | 🦄, 🦭, 🦔, 🪵 |
| capybara | No | 🦫, 🐾, 🦘, 🐰 |
| swordfish | No | 🐟, 🐠 |

### Question Types

| ID | Question | Presupposes Existence |
|----|----------|----------------------|
| Q0 | Is there an official {animal} emoji in Unicode? | No |
| Q1 | Is there a {animal} emoji? | No |
| Q2 | Show me just the {animal} emoji? Only return an emoji nothing else. | Yes (strong) |
| Q3 | Show me just the {animal} emoji? Only return an emoji if it exists, or else 'None'. | Yes (with escape) |
| Q4 | What is the {animal} emoji? | Yes (strong) |
| Q5 | What does the {animal} emoji look like? | Yes (strong) |

## Summary by Model

| Model | B1: Wrong Belief | B2: Self-Correction | B3: Wrong Emoji | Total |
|-------|------------------|---------------------|-----------------|-------|
| INSTRUCT | 30/54 (56%) | 9/54 (17%) | 30/54 (56%) | 54 |
| BASE | 36/54 (67%) | 0/54 (0%) | 17/54 (31%) | 54 |

## By Question Type

| Question | Instruct B1 | Instruct B2 | Instruct B3 | Base B1 | Base B2 | Base B3 |
|----------|-------------|-------------|-------------|---------|---------|---------|
| Q0 | 2 | 1 | 2 | 5 | 0 | 0 |
| Q1 | 2 | 2 | 2 | 3 | 0 | 2 |
| Q2 | 7 | 0 | 7 | 7 | 0 | 7 |
| Q3 | 7 | 0 | 7 | 7 | 0 | 8 |
| Q4 | 6 | 3 | 6 | 7 | 0 | 0 |
| Q5 | 6 | 3 | 6 | 7 | 0 | 0 |

## By Animal

| Animal | Has Emoji | Instruct B1 | Instruct B2 | Instruct B3 | Base B1 | Base B2 | Base B3 |
|--------|-----------|-------------|-------------|-------------|---------|---------|---------|
| seahorse | No | 5 | 1 | 6 | 5 | 0 | 3 |
| octopus | Yes | 2 | 1 | 1 | 1 | 0 | 2 |
| axolotl | No | 4 | 2 | 4 | 4 | 0 | 2 |
| armadillo | No | 4 | 0 | 4 | 5 | 0 | 2 |
| snail | Yes | 1 | 1 | 1 | 1 | 0 | 0 |
| platypus | No | 4 | 2 | 4 | 5 | 0 | 2 |
| narwhal | No | 4 | 2 | 4 | 6 | 0 | 2 |
| capybara | No | 4 | 0 | 4 | 5 | 0 | 2 |
| swordfish | No | 2 | 0 | 2 | 4 | 0 | 2 |

## Question Type Reference

| ID | Question |
|----|----------|
| Q0 | Is there an official {animal} emoji in Unicode? |
| Q1 | Is there a {animal} emoji? |
| Q2 | Show me just the {animal} emoji? Only return an emoji nothing else. |
| Q3 | Show me just the {animal} emoji? Only return an emoji if it exists, or else 'None'. |
| Q4 | What is the {animal} emoji? |
| Q5 | What does the {animal} emoji look like? |

## Behavior Definitions

| Code | Behavior | Description |
|------|----------|-------------|
| B1 | Wrong Belief | Believes non-existent emoji exists, or real emoji doesn't exist |
| B2 | Self-Correction | Gets into loops like 'wait that's not it', contradicts itself |
| B3 | Wrong Emoji | Outputs incorrect emoji character |
