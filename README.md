# PokeDash-AI: An Artificial Intelligence Experiment
_Disclaimer: I would not consider this code clean and error-free, thus it is not structured for reuse by others. Additionally, I was not following the PEP 8 style of coding so common python community standards and conventions were not followed._
## Introduction
After completing an introductory course into Deep Learning, I finally had a basic understanding sufficient enough to start a project that I've been itching to do for a while. The challenge is simple: "Can I create an neural network that can learn to play a game?"

The first few weeks of 2019 was spent learning how to use [PyGame](https://www.pygame.org/docs/), an Open Source python package allowing user to design and build multimedia applications such as games. At the beginning of June, I gave myself two weeks to build the game then train a reinforcement learning algoritm ontop of it.

The chosen game was Google's hidden T-Rex Runner; a great source of distraction as you wait for your modem to restart. In order to not let my sample space be too large, I did not incorporate the ability to _duck_ or include flying obstacles (my 6GB of RAM would cry).

Thus, the model only needed to figure out when to jump, and when not to jump. Below is a snapshot of the hitboxes and a fictitious "view" from the player.

![Player View](visuals/manual_view.jpg)

**Overview of Model**:
* Inputs:
  - abc
* Outputs:
  - def

## Baselines

### Random Model
In order to accurately identifiy learning, I first built in a neural network that provides random inputs. Accordingly, it was observed that for each iteration of the game, a random model would rarely score above 100 and averaged a score of 90.

![Random Model](visuals/random_model.gif)

### Manual Model

Of course, it would be remiss of me to ask my model to solve something I could not conceptually solve. After going through a few iterations, it was found that a simplistic, but exceptonal, solution was jumping when an obstacle is equal to or less than 20 pixels away.

![Manual Model](visuals/manual_model.gif)

## DQN Model

A DQN (Deep Q-Network) uses neural networks to train an agent (our player) based on game states it has seen before. As more states are stores into memory, the DQN estimates the best possible action. For a more in-depth explaination, feel free to read [this](https://towardsdatascience.com/introduction-to-various-reinforcement-learning-algorithms-i-q-learning-sarsa-dqn-ddpg-72a5e0cb6287) _Towards Data Science_ article that touches on the topic.

In our game environment, values are assigned to each state with the intention of having the model estimate actions that would produce the highest value from the subsequent state.

## Results
![Historical Performance](visuals/history.png)

![DQN Model](visuals/best_model.gif)

## Key Takeaways

## Future Considerations

## References
* Inspiration for Python Code: https://github.com/shivamshekhar/Chrome-T-Rex-Rush
* DQN Implementation: https://jaromiru.com/2016/10/03/lets-make-a-dqn-implementation/
* Creating a custom GYM environment: https://www.novatec-gmbh.de/en/blog/creating-a-gym-environment/
* And many other articles including:
  - https://keon.io/deep-q-learning/
  - https://medium.com/@apoddar573/making-your-own-custom-environment-in-gym-c3b65ff8cdaa
  - https://skymind.ai/wiki/deep-reinforcement-learning
  - https://adventuresinmachinelearning.com/reinforcement-learning-tutorial-python-keras/
