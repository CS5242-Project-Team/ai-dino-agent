<img width="125" src="/assets/dino_img.png">

### Introduction
The AI Dino Agent is a computer program that plays the [Chrome Dino](https://en.wikipedia.org/wiki/Dinosaur_Game) game without any human aid. The goal of the agent is to primarily attain a good high score and also to play the game in a way that is indistinguishable from a human. 

### Usage
This project has only been tested with Windows. Therefore, ensure that you clone the repository in a Windows environment.

#### Setup
1. Clone the repository
2. Ensure **Python** version >= **3.6.8**
3. Install the relevant pip packages.    
    ```
    pip install -r requirements.txt
    ```
4. Run the Game
    ```
    python dino_agent.py
    ```

The agent in progress:

<p align="center">
    <img width="1080" src="/assets/dino-game.gif">   
</p>

### Approach

The game is simple in the sense that there are only two controls for the player - a jump command and a duck command. The Dino character jumps over obstacles and ducks away from flying creatures - birds etc based on the respective commands. Doing so for a considerable amount of time builds the score. 

#### Current Methods vs Our Method
There have been multiple attempts in solving the Dino game problem. These attempts revolve around the use of Reinforcement Learning and Q-Learning, thereby bypassing the need for a  labelled dataset. In place of a dataset, these techniques allow the agent to build proficiency by employing the use of repeated automated simulations. 

<p align="center">
    <img width="250" src="/assets/reinforcement.png">
</p>

However, in this project, we take a **different approach** - we convert the problem into an image classification task. This way, the challenge in turn becomes building a classifier that,  given a particular game state, classifies between three different moves - jump, duck or inaction. A game state here is represented by a fullscreen screenshot of the game in progress.

<p align="center">
    <img width="800" src="/assets/classification.JPG">
</p>

#### Simplifying the Problem
At this point, it was difficult to determine if converting it to a classification task would be sufficient for the agent to play somewhat well. 

The game naturally tends to increase the speed of the agent as the score increases. Since a static screenshot does not convey speed, we decided to **do away** with the speed aspect of the game for the time being. This way, the neural network would only learn to jump/duck for a single speed setting; constant speed of 6.

#### Encoding Speed

### Final Solution