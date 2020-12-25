from os import system,name
import time
from turtle import Turtle, Screen, Shape

#global variables
keypressed = False
wn = Screen()

# define our clear function 
def clear(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 



def main():
    
    global wn
    global keypressed
    point,z,a = 0,0,0     # variable declarations
    

    clear()
    width = 1000
    height = 700
  
    wn.setup(width, height)
    wn.bgcolor("black")                             #sets window background color to black
    wn.title("Welcome to Happy Hoppy!!")

    ls_names= []
    n= int(input("Enter number of players:(Max 5, Min 2)"))        
    
    if (n>5):
        print("You entered more than 5!")
        exit()
    else :
        print("Enter names of the players:")             # takes in list of names of players
        for i in range(n):
            f= "Player " + str(i+1) + ": "
            inp= input( f )
            ls_names.append(inp)

    lb = Leaderboard(ls_names)                         #creates instance of class Leaderboard


    while(1):

        if(z>=n):                             #display leaderboard after all players have played
            print("Leaderboard: ")            
            wn.clearscreen()
            wn.bgcolor("black")
            lb.display()
            break

        else: 

            print("It is " + ls_names[z]+ "'s turn to play !" )
            wn.clearscreen()
            wn.bgcolor("black")
            s = 0.01
            time.sleep(2)

            while(1):
                
                smiley = smiley_making()               #access turtle objects
                wall = wall_making()
                
                
                for i in range(1,45):
                    wall.penup()
                    wall.backward(i)
                    wn.listen()
                    wn.onkey(keypress, "space")           #listens for keypress
                    jumper = Jumper(smiley, 10, wn, -2 , 35 )   #instance of class Jumper 
                    if (keypressed):
                        if (i>28):                       # key pressed at right moment
                            jumper.jump()                 #calling jump function
                            point += 1
                            wn.clearscreen()
                            wn.bgcolor("black")
                            keypressed =False
                            if (s < 0.00001):            #manipulating speed of wall
                              z += 1
                              a = 1
                            s = s / 10
                            break
                            

                        else:
                            lb.update(ls_names[z], point)   #store points
                            if (z>=n):
                                a=1                   
                                keypressed = False
                                break
                                
                                
                            else: 
                                point =0                       #reset and shift to next player
                                z=z+1
                                a=1
                                keypressed = False
                                break


                    elif (wall.xcor() < smiley.xcor()):           
                        lb.update(ls_names[z], point)
                        if (z>=n):
                            
                            a=1
                            break         
                        else:
                            point=0
                            z=z+1
                            a=1
                            break
                    
                    time.sleep(s)

                        
                if (a==1):         # To shift control to last player/ exit out of innermost while loop
                    break
                else:
                    continue
                


class Leaderboard:
    
    def __init__(self, names):            
        """ constructor, get list of names and input when creating instance"""
        if not isinstance(names, list) or len(names) == 0:
            raise Exception("Please enter names AND NOTHING ELSE")
        self.leaderboard = {}
        for name in names:
            self.leaderboard[name] = 0
            
                  
    def update(self, name, score):
        """update given name with given score"""  
        self.leaderboard[name] = score
    
  
    def display(self):
        """displays name, score pair in order of descending scores """
        sNames = sorted(self.leaderboard.items(), key=lambda x: x[1], reverse=True)
        for name, score in sNames:
            print(name, score)
        print('Everyone is a winner! Life is not always about being the best!')
    
    def resetScores(self):
        """reset all scores to 0 while retaining names"""
        for name in self.leaderboard:
            self.leaderboard[name] = 0
            
  
    def wipe(self):
        """wipes leaderboard entirely (including names)"""
        self.leaderboard = {}


def smiley_making():
    """Drawing the smiley"""

    global wn
    
    shape = Shape('compound')
    smiley = Turtle(visible=False)
    smiley.speed('fastest')
    smiley.penup()
    #face 
    smiley.goto(215,0)

    smiley.begin_poly()
    smiley.circle(50) 
    smiley.end_poly()
    shape.addcomponent(smiley.get_poly(),'yellow')

    #first eye
    smiley.goto(200,25)
    smiley.begin_poly()
    smiley.circle(5) 
    smiley.end_poly()
    shape.addcomponent(smiley.get_poly(),'black')

    #second eye
    smiley.goto(200,50)
    smiley.begin_poly()
    smiley.circle(5) 
    smiley.end_poly()
    shape.addcomponent(smiley.get_poly(),'black')

    #mouth
    smiley.goto(230,40)
    smiley.begin_poly()
    smiley.goto(240,40)
    smiley.goto(240,50)
    smiley.goto(230,50)
    smiley.goto(230,40)
    smiley.end_poly
    shape.addcomponent(smiley.get_poly(),'red')

    wn.register_shape('smiley',shape)
    smiley.reset()
    smiley.shape('smiley')
    smiley.setposition(0,0) #not sure abt the coordinates
    smiley.penup()
    smiley.backward(500) 
    return smiley

def wall_making():
    """Drawing the rectangle"""
    global wn
    
    shape = Shape('compound')
    wall = Turtle(visible=False)
    wall.penup()
    wall.goto(200,100)
    wall.begin_poly()
    wall.goto(200,200)
    wall.goto(400,200)
    wall.goto(400,100)
    wall.goto(200,100)
    wall.penup()
    wall.end_poly()
    shape.addcomponent(wall.get_poly(),'yellow')
    wn.register_shape('rectangle',shape)
    wall.reset()
    wall.shape('rectangle')
    wall.setposition(70,0)
    
    return wall

        

class Jumper:
    
    def __init__ (self, t , xSpeed, win, grav, ySpeed):
        """max jump height and horizontal distance by kinematics equations"""
        self.t = t
        self.t.dx = xSpeed
        self.win = win
        self.grav = grav
        self.t.dy = ySpeed
        self.t.s = "r"
    
    def jump(self):
        """call wn.listen() and wn.onkey(jumper.jump) or wn.onkeypress(jumper.jump, key)"""
        if (self.t.s == "r"):
            self.t.penup()
            self.t.s = "j"
            oPos = self.t.ycor()
            dy = self.t.dy
            while True:
                dy += self.grav
                y = self.t.ycor()
                y += dy
                x = self.t.xcor()
                x += self.t.dx
                self.t.sety(y)
                self.t.setx(x)
                if (self.t.ycor() < oPos):
                    self.t.sety(oPos)
                    self.t.s = "r"
                    break
                self.win.update()

def keypress():
    global keypressed
    keypressed = True
    return keypressed

if __name__ == "__main__":
    main()
    
    
wn.mainloop()
