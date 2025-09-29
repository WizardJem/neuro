def calculate(a , b, c):
   if b == "+" :
     return a + c
   elif b == "-" :
      return a - c
   elif b == "/" :
       return a / c
   elif b == "*" :
      return a * c 
   
print(calculate(10, "+", 10))  # should return 20
print(calculate(10, "-", 10))  # should return 0
print(calculate(10, "*", 10))  # should return 100
print(calculate(10, "/", 10))  # should return 1.0
