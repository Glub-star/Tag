import turtle as t
from functools import partial
import threading
import time
import random

screen = t.Screen()

screen.setup(500,500) # Window Scale
screen.tracer(0,0)
screen.bgcolor("white")
t.listen()
FONT = ('Arial', 15, 'normal')
FPS = 400

score_turtle = t.Turtle()
score_turtle.penup()

class rect:
    def __init__(self, position_x = 0, position_y=0, size_x=10, size_y=10, rotation = 0, colour = "black") :
        self.x = position_x
        self.y = position_y
        self.size_x = size_x
        self.size_y = size_y
        self.rotation = rotation
        self.turtle = t.Turtle()
        self.turtle.ht()
        self.turtle.fillcolor(colour)
    
    def draw(self):
        self.turtle.fillcolor(self.colour)
        self.turtle.penup()
        self.turtle.setpos(self.x,self.y)
        self.turtle.pendown()
        self.turtle.begin_fill()
        self.turtle.setheading(self.rotation)
        for i in range(2):
            self.turtle.forward(self.size_x)
            self.turtle.right(90)
            self.turtle.forward(self.size_y)
            self.turtle.right(90)
        self.turtle.end_fill()
        self.turtle.penup()

class Player(rect):
    def __init__(self,colour = "black"):
        super().__init__()
        self.dx = 0
        self.dy = 0
        self.colour = colour
        self.score = 0
    def move(self, direction = (0,0)):
        self.dx = self.x + direction[0]
        self.dy = self.y + direction[1]
        if self.dy > 250:
            self.dy = 250 
        elif self.dy < -250 + self.size_y:
            self.dy = -250 + self.size_y
        elif self.dx > (250 - self.size_x):
            self.dx = 250 - self.size_x
        if self.dx < -250:
            self.dx = -250
        
        self.x = self.dx
        self.y = self.dy

def draw_scores():
    
    score_turtle.goto(-250,215)
    score_turtle.write(f"Red : {round(player_1.score,2)}", font = FONT)
    score_turtle.goto(-250, 200)
    score_turtle.write(f"Blue : {round(player_2.score,2)}", font = FONT)


#region Input system

# https://python-forum.io/thread-34100.html
class WatchedKey:
    def __init__(self, key):
        self.key = key
        self.down = False
        t.onkeypress(self.press, key)
        t.onkeyrelease(self.release, key)

    def press(self):
        self.down = True

    def release(self):
        self.down = False

keys_to_watch = {'w', 'a', 's', 'd', 'Up' , 'Down' , 'Left' , 'Right'}

watched_keys = {key: WatchedKey(key) for key in keys_to_watch}

#endregion

#region FPS organiser

# https://code.activestate.com/recipes/579053-high-precision-fps/history/2/
_tick2_frame=0
_tick2_fps=20000000 # real raw FPS
_tick2_t0=time.time()

def tick(fps=60):
 global _tick2_frame,_tick2_fps,_tick2_t0
 n=_tick2_fps/fps
 _tick2_frame+=n
 while n>0: n-=1
 if time.time()-_tick2_t0>1:
  _tick2_t0=time.time()
  _tick2_fps=_tick2_frame
  _tick2_frame=0

#endregion

game_loop = True
player_1 = Player(colour = "red")
player_2 = Player(colour = "blue")
frame = 0
t.ht()
projectiles = []
tag_cooldown = 1
tag_cooldown_time = tag_cooldown
tag = random.randint(1,2)

while game_loop:
    tick(FPS) # FPS limit
    player_speed = 500 / FPS

    if watched_keys['w'].down:
        player_1.move((0,player_speed))
    if watched_keys['s'].down:
        player_1.move((0,-player_speed))
    if watched_keys['a'].down:
        player_1.move((-player_speed,0))
    if watched_keys['d'].down:
        player_1.move((player_speed,0))
    #if watched_keys['space'].down:
    #    projectiles.append(rect(position_x=player.x,position_y = player.y,colour="lightblue"))
    
    if watched_keys['Up'].down:
        player_2.move((0,player_speed))
    if watched_keys['Down'].down:
        player_2.move((0,-player_speed))
    if watched_keys['Left'].down:
        player_2.move((-player_speed,0))
    if watched_keys['Right'].down:
        player_2.move((player_speed,0))

    if player_1.x < player_2.x+10 and player_1.x+10 > player_2.x and  player_1.y <player_2.y+10 and player_1.y+10 >player_2.y and tag_cooldown_time < 0:
        print("Collison! ")
        tag_cooldown_time = tag_cooldown
        tag += 1
        if tag == 3:
            tag = 1
    
    if tag == 1:
        player_1.colour = "yellow"
    else: 
        player_1.colour = "red"
        player_1.score += 1 / FPS
    if tag == 2:
        player_2.colour = "yellow" 
    else: 
        player_2.colour = "blue"
        player_2.score += 1 / FPS

    player_1.draw()
    player_2.draw()
    for i in projectiles:
        i.draw()
    
    frame +=1
    
    draw_scores()
    keys= []
    t.update()
    player_1.turtle.clear()
    player_2.turtle.clear()
    tag_cooldown_time -= 1 / 60
    #print(f"tag cooldown : {tag_cooldown_time}")
    #print(f"Frame {frame} done")
    t.clear()
    score_turtle.clear()
    
