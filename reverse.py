print("Enter String to reverse")
a= input("")
print("You Entered:->",a)
rev=""
for i in a:
	rev=i+rev
print(f"reverse of",a, "is",rev)