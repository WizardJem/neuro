import random


print("Enter your name:")
name = input()


crea = ['Giraffe', 'Jaguar', 'Orca', 'Rhinoceros', "Dolphin", "Lion"]
a =random.choice(crea)

adj = ['Handsome', 'Fast', 'Mighty', 'Weak', "Cunning", "Terrible"]
b =random.choice(adj)
c = random.randint(0, 100)
print ( f"{name}, You are agent {c} with the codename: {b} {a}")