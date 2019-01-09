from graphics import *

win = GraphWin('Calculator', width=200, height=200)  # create a window
win.setBackground('white')
win.setCoords(0, 0, 12, 12)

text_area = Text(Point(2, 11), "")
text_area.setFill('blue')
text_area.draw(win)


def numeric_buttons():
    button_color = 'black'
    # x,y  x,y

    _1 = Rectangle(Point(0.25, 0.25), Point(2.25, 2.25))
    _1.setFill(button_color)
    _1.draw(win)

    _1_t = Text(_1.getCenter(), "1")
    _1_t.setFill('white')
    _1_t.draw(win)

    _2 = Rectangle(Point(2.5, 0.25), Point(4.5, 2.25))
    _2.setFill(button_color)
    _2.draw(win)

    _2_t = Text(_2.getCenter(), "2")
    _2_t.setFill('white')
    _2_t.draw(win)

    _plus = Rectangle(Point(4.75, 0.25), Point(6.75, 2.25))
    _plus.setFill(button_color)
    _plus.draw(win)

    _plus_t = Text(_plus.getCenter(), "+")
    _plus_t.setFill('white')
    _plus_t.draw(win)

    _equals = Rectangle(Point(7, 0.25), Point(9.25, 2.25))
    _equals.setFill(button_color)
    _equals.draw(win)

    _equals_t = Text(_equals.getCenter(), "=")
    _equals_t.setFill('white')
    _equals_t.draw(win)

    return _1, _2, _plus, _equals


def inside(point, rectangle):
    ll = rectangle.getP1()
    ur = rectangle.getP2()
    return ll.getX() < point.getX() < ur.getX() and ll.getY() < point.getY() < ur.getY()


_1, _2, _plus, _equals = numeric_buttons()


def getClickedButton(clickPoint):
    if clickPoint is None:
        pass
    elif inside(clickPoint, _1):
        return '1'
    elif inside(clickPoint, _2):
        return '2'
    elif inside(clickPoint, _plus):
        return '+'
    elif inside(clickPoint, _equals):
        return '='


equation = ''

while True:

    if '=' in equation:
        equation = ''

    clickPoint = win.getMouse()
    value = getClickedButton(clickPoint)
    if value != '=':
        equation += value
        print equation
    else:
        print 'To be evaluated: ' + equation
        answer = str(eval(equation))
        equation = '{0}={1}'.format(equation, answer)

    text_area.setText(equation)



win.close()
