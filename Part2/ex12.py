
def check(str):
    if str.startswith("The") :
        return ("Found You.")
    else :
        return ("You are safe. For now.")

str1 = 'The'
str2 = 'Thumbs up'
str3 = 'Theatre can be boring'

print(check(str1)) 
print(check(str2)) 
print(check(str3))  