'''Final project for intro CS'''
import turtle
import tkinter as tk
import tkinter.messagebox
from random import uniform
from time import sleep

'''
Screen Numbers:

-1 = Quit
0 = Title
1 = Singleplayer Pong
2 = Multiplayer Pong
3 = Game over
4 = Scores
'''

# screenNum controls screen transitions
# playerWin dictates which player has won 
# difficult flags if the player has selected the "difficult" option
# score initializes Player A's and Player B's scores
# DEFAULT_FONT sets the font across all screens unless manually specified

screenNum = 0
playerWin = None
difficult = False
score = [0, 0]
DEFAULT_FONT = "Helvetica"

# Game Objects  
class ScoreBoard:

    def __init__(self):
        self.resetScore()

        self.pen = turtle.Turtle()
        self.pen.color("white")
        self.pen.speed(0)
        self.pen.hideturtle()
        self.pen.penup()
        self.pen.goto(0, 260)
    
    def displayScore(self, align: str, font: str, fontsize: int):
        self.pen.write(f"Player A: {score[0]}\tPlayer B: {score[1]}", align=align, font=(font, fontsize, "normal"))
    
    def addPlayer1Score(self, x=1):

        score[0] += x
        self.pen.clear()
        self.displayScore("center", DEFAULT_FONT, 24)

    def addPlayer2Score(self, x=1):

        score[1] += x
        self.pen.clear()
        self.displayScore("center", DEFAULT_FONT, 24)  

    def getPlayer1Score(self):
        return score[0]
    
    def getPlayer2Score(self):
        return score[1]

    def resetScore(self):
        for i in range(len(score)):
            score[i] = 0
    
    def hide(self):
        self.pen.clear()



class Paddle:

    def __init__(self, x: float, color="white"):

        self.paddle = turtle.Turtle()
        self.paddle.shape("square")
        self.paddle.shapesize(stretch_wid=5, stretch_len=1)
        self.paddle.color(color)
        self.paddle.penup()

        self.x = x
        self.paddle.goto(self.x, 0)
 
    def move(self, y: float):
        
        self.paddle.sety(self.paddle.ycor() + y)

        if self.paddle.ycor() > 240:
            self.paddle.sety(240)

        if self.paddle.ycor() < -240:
            self.paddle.sety(-240)

    def up(self):
        self.move(20)
    
    def down(self):
        self.move(-20)
    
    def get_ycor(self):
        return self.paddle.ycor()
    
    def reset_position(self):
        self.paddle.goto(self.x, 0)
    
    def hide(self):
        self.paddle.hideturtle()



class Bot(Paddle):
    
    def __init__(self, x: float, speed: float, color="white"):
        super().__init__(x, color)
        self.speed = speed
    
    # Control the speed of bot by overriding Paddle functions
    def up(self):
        self.move(self.speed)
    
    def down(self):
        self.move(-self.speed)



class Ball:

    BALL_STARTING_SPEED = .2
    BALL_INCR_SPEED = .05

    def __init__(self, color="white"):

        self.ball = turtle.Turtle()
        self.ball.shape("circle")
        self.ball.color(color)
        self.ball.penup()
        self.ball.goto(0, 0)
        self.ball.speed(0)

        self.dx = Ball.BALL_STARTING_SPEED
        self.dy = Ball.BALL_STARTING_SPEED
      
    def move(self):
        self.ball.setx(self.ball.xcor() + self.dx)
        self.ball.sety(self.ball.ycor() + self.dy)

    def get_xcor(self):
        return self.ball.xcor()

    def get_ycor(self):
        return self.ball.ycor()
    
    def reset_position(self):
        self.ball.goto(0, 0)
    
    def startPositiveDir(self):
        self.dx = Ball.BALL_STARTING_SPEED
        self.dy = Ball.BALL_STARTING_SPEED

    def startNegativeDir(self):
        self.dx = -Ball.BALL_STARTING_SPEED
        self.dy = -Ball.BALL_STARTING_SPEED

    def hide(self):
        self.ball.hideturtle()
    
    def bounceDown(self):
        self.ball.sety(290)
        self.dy *= -1
    
    def bounceUp(self):
        self.ball.sety(-290)
        self.dy *= -1
    
    def bouncePaddleLeft(self):
        self.dx -= uniform(0, Ball.BALL_INCR_SPEED)
        self.dx *= -1
        self.ball.setx(-340)
    
    def bouncePaddleRight(self):
        self.dx += uniform(0, Ball.BALL_INCR_SPEED)
        self.dx *= -1
        self.ball.setx(340)
    
    def get_dx(self):
        return self.dx



class Arrow:

    def __init__(self, start_direction="right"):

        self.arrow_head = turtle.Turtle()
        self.arrow_head.shape("arrow")
        self.arrow_head.shapesize(1)
        self.arrow_head.color("white")
        self.arrow_head.penup()
        self.arrow_head.speed(0)

        self.arrow_base = turtle.Turtle()
        self.arrow_base.shape("square")
        self.arrow_base.shapesize(.2, 1.6)
        self.arrow_base.color("white")
        self.arrow_base.penup()
        self.arrow_base.speed(0)

        self.show(start_direction)

    def hide(self):
        self.arrow_head.hideturtle()
        self.arrow_base.hideturtle()
    
    def show(self, direction: str):

        if direction == "left":
            self.arrow_head.goto(-50, -50)
            self.arrow_head.setheading(225)

            self.arrow_base.goto(-40, -40)
            self.arrow_base.setheading(225)
        
        if direction == "right":
            self.arrow_head.goto(50, 50)
            self.arrow_head.setheading(45)

            self.arrow_base.goto(40, 40)
            self.arrow_base.setheading(45)

        self.arrow_head.showturtle()
        self.arrow_base.showturtle()



# Screen Objects
# Instance class sets up basic window
class Screen:

    def __init__(self):

        self.wn = turtle.Screen()
        self.wn.setup(width=800, height=600)
        self.wn.title("Pong")
        self.wn.bgcolor("black")
        self.wn.tracer(0)

        self.canvas = self.wn.getcanvas()
    
    def _hide_widget(self, *args):
        for widget in args:
            widget.destroy()
    
    def _esc_click(self):
        global screenNum
        screenNum = -1



class TitleScreen(Screen):
    
    def __init__(self):
        super().__init__()

        self.pen = turtle.Turtle()
        self.pen.color("white")
        self.pen.speed(0)
        self.pen.hideturtle()
        self.pen.penup()

        self.pen.goto(0, 230)
        self.pen.write("Welcome to Pong!", align="center", font=(DEFAULT_FONT, 24))

        self.pen.goto(0, 200)
        self.pen.write("Left Paddle: (w, s)\tRight Paddle: (Up, Down)", align="center", font=(DEFAULT_FONT, 16))

        self.pen.goto(0, 170)
        self.pen.write(f"Score {PongScreen.POINTS_TO_WIN} points to win!", align="center", font=(DEFAULT_FONT, 16))

        self.s1_button = tk.Button(self.canvas.master, width=18, height=1, text="Singleplayer (Normal)", font=(DEFAULT_FONT, 24), bg="grey", bd=6, command=self._s1_click)
        self.s1_button.place(x=219, y=170)

        self.s2_button = tk.Button(self.canvas.master, width=18, height=1, text="Singleplayer (Difficult)", font=(DEFAULT_FONT, 24), bg="grey", bd=6, command=self._s2_click)
        self.s2_button.place(x=219, y=250)

        self.m_button = tk.Button(self.canvas.master, width=18, height=1, text="Multiplayer", font=(DEFAULT_FONT, 24), bg="grey", bd=6, command=self._m_click)
        self.m_button.place(x=219, y=330)

        self.score_button = tk.Button(self.canvas.master, width=18, height=1, text="See Scores", font=(DEFAULT_FONT, 24), bg="grey", bd=6, command=self._score_click)
        self.score_button.place(x=219, y=410)

    # Click Event Functions
    def _s1_click(self):
        self.pen.clear()
        self._hide_widget(self.s1_button, self.s2_button, self.m_button, self.score_button)
        
        global screenNum
        global difficult
        difficult = False
        screenNum = 1
    
    def _s2_click(self):
        self.pen.clear()
        self._hide_widget(self.s1_button, self.s2_button, self.m_button, self.score_button)
        
        global screenNum
        global difficult
        difficult = True
        screenNum = 1
    
    def _m_click(self):
        self.pen.clear()
        self._hide_widget(self.s1_button, self.s2_button, self.m_button, self.score_button)

        global screenNum
        screenNum = 2
    
    def _score_click(self):
        self.pen.clear()
        self._hide_widget(self.s1_button, self.s2_button, self.m_button, self.score_button)

        global screenNum
        screenNum = 4




class ScoreScreen(Screen):

    def __init__(self):
        super().__init__()

        self.pen = turtle.Turtle()
        self.pen.color("white")
        self.pen.hideturtle()
        self.pen.penup()
        self.pen.goto(0, 230)
        self.pen.write("Pong Scores:", align="center", font=(DEFAULT_FONT, 24, "normal"))

        self.t_button = tk.Button(self.canvas.master, width=12, height=1, text="Return to Title", font=(DEFAULT_FONT, 24), bg="grey", bd=6, command=self._t_click)
        self.t_button.place(x=100, y=250)
        
        self.y_scroll = tk.Scrollbar(self.canvas.master, orient="vertical")
        self.score_output = tk.Text(self.canvas.master, bg="white", bd=3, width=20, height=15, font=(DEFAULT_FONT, 16), yscrollcommand=self.y_scroll.set)
        
        self.y_scroll.config(command=self.score_output.yview)
        self.score_output.place(x=445, y=130)

        self._display_scores()
    
    def _t_click(self):
        self.pen.clear()
        self._hide_widget(self.t_button, self.y_scroll, self.score_output)

        global screenNum
        screenNum = 0
    
    def _display_scores(self):

        try:
            self.score_file = open("scores.txt", "r")
            self.score_list = self.score_file.readlines()
            self.score_list.reverse()
            for line in self.score_list:
                self.score_output.insert(tk.END, line)
            
            self.score_file.close()
        
        except FileNotFoundError:
            tkinter.messagebox.showerror(message="Score file not found!")
        
        finally:
            self.score_output.config(state="disabled")


# Instance Class with Pong game handlers
class PongScreen(Screen):

    # The amount of points required for the game to end
    POINTS_TO_WIN = 11

    def __init__(self):
        super().__init__()
        
        self.ball = Ball()
        self.arrow = Arrow()
        self.paddleRight = Paddle(350, "blue")
        self.paddleLeft = Paddle(-350)
        self.scoreBoard = ScoreBoard()

    # Game Handlers
    def checkBorderCollision(self):

        # Check for screen borders
        # If left or right border, reset ball to center and add score
        # If top or bottom border, ricochet ball

        if self.ball.get_xcor() > 390:
            
            self.ball.reset_position()
            self.arrow.show(direction="right")
            self.paddleLeft.reset_position()
            self.paddleRight.reset_position()
            self.scoreBoard.addPlayer1Score()

            self.paddleLeft.paddle.color("white")
            self.paddleRight.paddle.color("blue")

            self.wn.update()
            sleep(.5)
            self.ball.startPositiveDir()
            self.arrow.hide()
        
        if self.ball.get_xcor() < -390:

            self.ball.reset_position()
            self.arrow.show(direction="left")
            self.paddleLeft.reset_position()
            self.paddleRight.reset_position()
            self.scoreBoard.addPlayer2Score()

            self.paddleLeft.paddle.color("blue")
            self.paddleRight.paddle.color("white")

            self.wn.update()
            sleep(.5)
            self.ball.startNegativeDir()
            self.arrow.hide()
        
        if self.ball.get_ycor() > 290:
            self.ball.bounceDown()
        
        if self.ball.get_ycor() < -290:
            self.ball.bounceUp()     

    def checkPaddleCollision(self):

        if (self.ball.get_xcor() < -340 and self.ball.get_xcor() > -350) and (self.ball.get_ycor() > self.paddleLeft.get_ycor() - 40) and (self.ball.get_ycor() < self.paddleLeft.get_ycor() + 40):
            self.ball.bouncePaddleLeft()

            self.paddleLeft.paddle.color("white")
            self.paddleRight.paddle.color("blue")

        if (self.ball.get_xcor() > 340 and self.ball.get_xcor() < 350) and (self.ball.get_ycor() > self.paddleRight.get_ycor() - 40) and (self.ball.get_ycor() < self.paddleRight.get_ycor() + 40):
            self.ball.bouncePaddleRight()

            self.paddleLeft.paddle.color("blue")
            self.paddleRight.paddle.color("white")
    
    def winCondition(self, winScore):
        if score[0] < winScore and score[1] < winScore:
            return False
        else:
            return True 
    
    def _suppress_p1_key_events(self):
        self.wn.onkeypress(None, "w")
        self.wn.onkeypress(None, "s")
    
    def _suppress_p2_key_events(self):
        self.wn.onkeypress(None, "Up")
        self.wn.onkeypress(None, "Down")
        



class SingleplayerPongScreen(PongScreen):

    def __init__(self, botSpeed: float):
        super().__init__()
        self.paddleRight.hide()

        self.paddleRight = Bot(350, speed=botSpeed, color="blue")
    
    def botAi(self):
        
        if self.ball.get_xcor() > -100:
                
                if self.ball.get_ycor() < self.paddleRight.get_ycor():
                    self.paddleRight.down()
                
                if self.ball.get_ycor() >= self.paddleRight.get_ycor():
                    self.paddleRight.up()
    
    def run(self):
        
        global screenNum
        global playerWin

        self.scoreBoard.displayScore("center", DEFAULT_FONT, 24)

        # Listen for key presses
        self.wn.listen()
        self.wn.onkeypress(self.paddleLeft.up, "w")
        self.wn.onkeypress(self.paddleLeft.down, "s")

        self.wn.update()
        sleep(1.5)
        self.arrow.hide()

        while screenNum == 1:

            # Score Limit
            if not self.winCondition(PongScreen.POINTS_TO_WIN): 
                
                self.wn.update()
                self.ball.move()
                self.checkBorderCollision()
                self.checkPaddleCollision()

                # Bot Paddle
                self.botAi()

            else:   # <-- If a player has won, change screen to EndScreen
                self.wn.update()
                sleep(.5)
                self.ball.hide()
                self.arrow.hide()
                self.paddleLeft.hide()
                self.paddleRight.hide()
                self.scoreBoard.hide()

                if score[0] == PongScreen.POINTS_TO_WIN:
                    playerWin = "A"
                
                else:
                    playerWin = "B"
                        
                screenNum = 3



class MultiplayerPongScreen(PongScreen):

    def __init__(self):
        super().__init__()
     
    def run(self):

        global screenNum
        global playerWin

        self.scoreBoard.displayScore("center", DEFAULT_FONT, 24)

        # Listen for key presses
        self.wn.listen()
        
        # Wait 1.5 seconds before starting
        self.wn.update()
        sleep(1.5)
        self.arrow.hide()

        # Game Loop
        while screenNum == 2:

            # Score Limit
            if not self.winCondition(PongScreen.POINTS_TO_WIN): 
                self.wn.update()
                self.ball.move()
                self.checkBorderCollision()
                self.checkPaddleCollision()

                # If the ball is moving left, Player 1 gains control
                # If the ball is moving right, Player 2 gains control
                if self.ball.get_dx() < 0:
                    self._suppress_p2_key_events()
                    self.wn.onkeypress(self.paddleLeft.up, "w")
                    self.wn.onkeypress(self.paddleLeft.down, "s")
        
                else:
                    self._suppress_p1_key_events()
                    self.wn.onkeypress(self.paddleRight.up, "Up")
                    self.wn.onkeypress(self.paddleRight.down, "Down")
                
            else:   # <-- If a player has won, change screen to EndScreen
                self.wn.update()
                sleep(.5)
                self.ball.hide()
                self.paddleLeft.hide()
                self.paddleRight.hide()
                self.scoreBoard.hide()

                if score[0] == PongScreen.POINTS_TO_WIN:
                    playerWin = "A"
                
                else:
                    playerWin = "B"
                
                screenNum = 3
            


class EndScreen(Screen):
    
    def __init__(self):
        super().__init__()

        self.pen = turtle.Turtle()
        self.pen.color("white")
        self.pen.speed(0)
        self.pen.hideturtle()
        self.pen.penup()

        self.pen.goto(0, 230)
        self.pen.write(f"Player {playerWin} has Won!\t{score[0]} - {score[1]}", align="center", font=(DEFAULT_FONT, 24))

        self.t_button = tk.Button(self.canvas.master, width=18, height=1, text="Return to Title Screen", font=(DEFAULT_FONT, 24), bg="grey", bd=6, command=self._t_click)
        self.t_button.place(x=219, y=170)

        self.save_button = tk.Button(self.canvas.master, width=18, height=1, text="Save Scores", font=(DEFAULT_FONT, 24), bg="grey", bd=6, command=self._save_click)
        self.save_button.place(x=219, y=250)

        self.clear_button = tk.Button(self.canvas.master, width=18, height=1, text="Clear Scores", font=(DEFAULT_FONT, 24), bg="grey", bd=6, command=self._clear_click)
        self.clear_button.place(x=219, y=330)

        self.wn.onkeypress(self._esc_click, "Escape")

        self._saved = False
        self.score_file = open("scores.txt", "a")

    # Click Event Functions
    def _t_click(self):
        self.pen.clear()
        self._hide_widget(self.t_button, self.save_button, self.clear_button)
        self.score_file.close()

        global screenNum
        screenNum = 0
    
    def _save_click(self):
        if not self._saved:
            self.score_file.write(f"Player A: {score[0]}\tPlayer B: {score[1]}\n")
            self._saved = True

            self.save_button.config(text="Saved!", state="disabled")
    
    def _clear_click(self):
        self.score_file.truncate(0)
        self.clear_button.config(text="Cleared!", state="disabled")

        

# Driver
def main():

    # Game Loop
    while screenNum >= 0:

        '''TITLE SCREEN'''
        if screenNum == 0:
            titleScreen = TitleScreen()
            
            while screenNum == 0:
                titleScreen.wn.update()

        '''SINGLEPLAYER'''
        if screenNum == 1:

            if not difficult:
                singleplayerScreen = SingleplayerPongScreen(botSpeed=.2)
            else:
                singleplayerScreen = SingleplayerPongScreen(botSpeed=.7)

            while screenNum == 1:
                singleplayerScreen.run()

        '''MULTIPLAYER'''
        if screenNum == 2:
            multiplayerScreen = MultiplayerPongScreen()

            while screenNum == 2:
                multiplayerScreen.run() 

        '''GAME OVER'''
        if screenNum == 3:
            gameOverScreen = EndScreen()
            
            while screenNum == 3:
                gameOverScreen.wn.update()
        
        '''SCORES'''
        if screenNum == 4:
            scoreScreen = ScoreScreen()

            while screenNum == 4:
                scoreScreen.wn.update()
        

    
if __name__ == "__main__":
    main()
