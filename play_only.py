import GTC as gtc
x = gtc.ureal(0.0,0.1,5)
y = gtc.ureal(0.0,0.2,10)
a =  x*y
print(a.u)
b = gtc.function.mul2(x, y)
print(b)

ab =gtc.result(a*b, label='result')
print(ab.label,ab)