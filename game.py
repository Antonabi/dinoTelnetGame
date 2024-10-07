import engine
import os
import time
import random
from rich import print
from typing import List

class Game:
    def __init__(self) -> None:
        self.window = engine.Window(70, 6)

        self.score = 0
        self.started = False

        # player
        self.player = self.window.addObject(["|", "P"], 5, self.window.height - 1)
        self.jumped = False

        self.gravity = 0.2

        # obstacles
        self.obstacles: List[engine.Object] = []
        for obstacle in range(5):
            obstacle = self.window.addObject(["O", "O"], self.window.width, self.window.height - 1)
            self.obstacles.append(obstacle)

    def tick(self):
        """
        Runs one step of the game (basically one frame). (Handles player and obstacles and increments the score)
        """
        if self.started:
            self.handlePlayer()
            self.handleObstacles()

            self.score += 1
    
    def handlePlayer(self):
        if self.jumped:
            self.jumped = False # so the jumps dont get queued
            if self.player.yPos >= self.window.height - 1:
                self.player.yVelocity = -2

        # update the players position based on velocity
        self.player.yPos += self.player.yVelocity

        # apply gravity to the velocity
        if self.player.yPos < self.window.height - 1:  # prevent going out of bounds
            self.player.yVelocity += self.gravity
        else:
            self.player.yPos = self.window.height - 1  # stay on the ground
            self.player.yVelocity = 0  # reset velocity when on the ground

    def handleObstacles(self):
        for obstacle in self.obstacles:
            if obstacle.xPos == self.player.xPos and obstacle.yPos == self.player.yPos: # collision detection
                self.__init__() # if the player collides, reset the class
            if obstacle.xPos < -1:
                obstacle.xPos = self.window.width # reset the obstacle to the starting point if out of bounds
            if obstacle.xPos > self.window.width - 1:
                if random.random() < 0.10: # 10% probability to move (spawn) the obstacle
                    obstacle.xPos -= 1
            else:
                obstacle.xPos -= 0.5 # if the obstacle is visible (moved or spawned, what you want to call it), move it

if __name__ == "__main__":
    # for testing out the output
    game = Game()
    while True:
        game.tick()
        time.sleep(0.02)
        os.system("clear")
        print(game.window.render())