---
title: The Monty Hall problem
date: April 18, 2025
description: An intuitive explanation for why switching doors improves your odds.
---

# The need for an intuitive explanation

I truly understand a topic when it *just* intuitively makes sense, almost like System 1 thinking. I do not need to derive it or think from an alternative perspective for it to make sense. One could argue that this may not be true for all things under the sun, like quantum physics, but I would argue back that I most definitely do not understand it.

But the Monty Hall problem is no string theory or quantum theory. Heck, it is not even an exponential! It is only probability and, given my day job, I am embarrassed to admit to myself that maybe I do not understand it as well as I think I do.

I have fallen into this weird cycle: I go over the problem, instinctively reject the correct solution, spend a long time thinking about it from different angles, and eventually convince myself of the correct answer. Then, one or two years later, I return to it and the answer still takes too much brain power to reach. It is far from the intuitive understanding I want.

I believe English, or any language, is a neat tool for understanding maths. If we can explain an idea in plain words, we can substitute symbols for those words and phrase it as a mathematical problem. So I decided to write about how I understand the solution, so that I can spot any inconsistencies or gaps. I can also return to it the next time I find myself struggling with it, which I am convinced will happen.

# The very short explanation

The player chooses a door with the car. Since they already have the right door, they should not switch.

The player chooses a door with a goat. Since they have the wrong door, and Monty opens the only other wrong door, leaving the car door unopened, they should definitely switch.

Since the second scenario is more common—two thirds versus one third—it makes sense to switch.

# The longer explanation

*The game from the player's perspective:*

The player chooses a door at random. Monty shows a goat. The player chooses to stay or switch.

*The game from Monty's perspective:*

The player chooses a door, then Monty chooses one of the remaining doors so that it reveals a goat. If the player chose the car, Monty can choose either remaining door because both have goats. If the player chose a goat, Monty has no choice: he must open the door with the other goat. The door Monty did not open must therefore have the car.

Now that we know Monty's perspective and his limited choice when the player chooses a goat, let us revisit the player's perspective:

- If the player picks the right door—the car—Monty shows a goat, and the other closed door is also a goat.
- If the player picks the wrong door—a goat—Monty is forced to open the door with the other goat. The other closed door that Monty **could not open** has to be the car.

Now assign probabilities. There is a one-third probability of choosing the car door and a two-thirds probability of choosing a goat door. Two thirds of the time, Monty has no choice and the door he does not open must be the car. So we should switch.

# The extreme example

Replay the game with 100 doors: 99 goats and one car. We choose one door, then Monty opens 98 doors with goats. Should we switch?

There is only a 1% chance that we picked the door with the car, and a 99% chance that we picked a goat. In those 99% of cases, the door Monty did not open has the car.

# The conditional probability tree diagram

To be added.

# Other probability topics that stumped me

## Confidence intervals

A 95% confidence interval does not mean that there is a 95% chance that the true value is in your confidence interval.

Instead, it means that if you ran your experiment 100 times and calculated the confidence interval each time, around 95 of those intervals would contain the true value.

## Gaussian distribution and the Central Limit Theorem

To be added.




# Enrich Further
- [Rong and Reasonable, chapter 39](https://medium.com/@guha.ashwin/rong-but-reasonable-chapter-39-e62c0cc832db)
- [Video explanation](https://www.youtube.com/watch?v=_YRfSe-f1FE)
