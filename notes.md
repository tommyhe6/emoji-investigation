FAIL
other mandela effects other than seahorse emoji did not cause issues naively
qwen3-4B-instruct nails 2 digit multiplication -> was not able to get it to fail consistently with a system prompt.
qwen3-4B-instruct fails consistently on 3 digit multiplication. -> reasoning models nail 3 digit multiplication

SUCCESS
list all emojis caused it to get stuck on 1 emoji
asking it if seahorse emoji exists causes it to freak out

TASK:
Why does asking the model about the seahorse emoji cause it to hallucinate but also continuously correct itself? Sometimes corrects itself multiple times with incorrect emojis. Sometimes corrects itself once and moves one. Sometimes gets stuck in a loop. Many animal emojis in general cause problems around hallucination and similar correction behavior, such as swordfish.
