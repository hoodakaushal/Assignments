__author__ = 'hooda'

def f(b,x):
    x2 = b*x*(1-x)

    while True:
        print(x2)
        x3 = b*x2*(1-x2)
        x2 = x3
        s = raw_input()
