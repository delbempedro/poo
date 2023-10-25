somevalues = list(map(lambda y: y ** 2 - 1, 
                      filter(lambda x: x % 5 == 0, range(20))))
print(somevalues)

somevalues = []
for i in range(20):
	x = i**2-1
	if x not in somevalues and i%5 == 0:
		somevalues.append(x)
print(somevalues)

somevalues = [i**2-1 for i in range(20) if i%5==0]
print(somevalues)
