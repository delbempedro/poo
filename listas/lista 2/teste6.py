values = list(filter(lambda x: x % 5 == 0, 
                     map(lambda y: y ** 2 - 1, range(20))))
print(values)

y = []
for i in range(20):
	y.append(i**2-1)
values = []
for j in y:
	if j%5==0:
		values.append(j)
print(values)

values = [y ** 2 - 1 for y in range(20) if (x := y ** 2 - 1) % 5 == 0]
print(values)
