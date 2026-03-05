import turtle
import random

screen = turtle.Screen()
screen.bgcolor('black')
screen.title('Fractal Tree')

pen = turtle.Turtle()
pen.hideturtle()
pen.setheading(90)
pen.color("white")
pen.speed(7)

def draw_branch(branch_length, pen_size):
    if branch_length < 15:
        pen.color(random.choice(["spring green", "lawn green"]))
        pen.stamp()
        pen.color("saddle brown")
        return

    pen.pensize(pen_size)
    pen.color("saddle brown")
    pen.forward(branch_length)

    new_length = branch_length * random.uniform(0.7, 0.9)
    right_angle = random.randint(15, 35)
    left_angle = random.randint(15, 35)

    pen.right(right_angle)
    draw_branch(new_length, pen_size * 0.7)

    pen.left(right_angle + left_angle)
    draw_branch(new_length, pen_size * 0.7)

    pen.right(left_angle)
    pen.backward(branch_length)

pen.penup()
pen.goto(0, -300)
pen.pendown()

draw_branch(120, 10)

turtle.done()