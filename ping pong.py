import tkinter as tk

# Setup the main window
window = tk.Tk()
window.title("Ping Pong Game")
window.resizable(False, False)

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_SIZE = 20

# Paddle Class
class Paddle:
    def __init__(self, canvas):
        self.canvas = canvas
        self.paddle = canvas.create_rectangle(0, 0, PADDLE_WIDTH, PADDLE_HEIGHT, fill="blue")
        self.canvas.move(self.paddle, (WINDOW_WIDTH - PADDLE_WIDTH) // 2, WINDOW_HEIGHT - 40)
        self.x_velocity = 0
        self.canvas_width = self.canvas.winfo_width()
        self.update_position()

    def move_left(self, event):
        self.x_velocity = -10

    def move_right(self, event):
        self.x_velocity = 10

    def stop_moving(self, event):
        self.x_velocity = 0

    def update_position(self):
        self.canvas.move(self.paddle, self.x_velocity, 0)
        pos = self.canvas.coords(self.paddle)
        if pos[0] <= 0:
            self.x_velocity = 0
        elif pos[2] >= self.canvas_width:
            self.x_velocity = 0

        self.canvas.after(20, self.update_position)

# Ball Class
class Ball:
    def __init__(self, canvas, paddle):
        self.canvas = canvas
        self.paddle = paddle
        self.ball = canvas.create_oval(0, 0, BALL_SIZE, BALL_SIZE, fill="red")
        self.canvas.move(self.ball, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.x_velocity = 5
        self.y_velocity = -5
        self.update_position()

    def update_position(self):
        self.canvas.move(self.ball, self.x_velocity, self.y_velocity)
        pos = self.canvas.coords(self.ball)
        paddle_pos = self.canvas.coords(self.paddle.paddle)

        # Ball collision with walls
        if pos[0] <= 0 or pos[2] >= WINDOW_WIDTH:
            self.x_velocity = -self.x_velocity
        if pos[1] <= 0:
            self.y_velocity = -self.y_velocity

        # Ball collision with the paddle
        if (paddle_pos[0] < pos[2] < paddle_pos[2]) and (paddle_pos[1] < pos[3] < paddle_pos[3]):
            self.y_velocity = -self.y_velocity

        # Ball falls off the screen (Game Over)
        if pos[3] >= WINDOW_HEIGHT:
            self.canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, text="Game Over", font=("Arial", 24), fill="red")
            return

        self.canvas.after(20, self.update_position)

# Create the game canvas
canvas = tk.Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="black")
canvas.pack()

# Create Paddle and Ball objects
paddle = Paddle(canvas)
ball = Ball(canvas, paddle)

# Keyboard bindings
window.bind("<Left>", paddle.move_left)
window.bind("<Right>", paddle.move_right)
window.bind("<KeyRelease>", paddle.stop_moving)

# Start the game loop
window.mainloop()
