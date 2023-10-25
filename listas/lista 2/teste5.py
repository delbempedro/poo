s = 0
for i in range(50):
    if i % 3 == 0 or i % 5 == 0:
        s += i * i
print(s)

def soma(i):
	for i in range(i):
		if i % 3 == 0 or i % 5 == 0:
			yield i*i
s = sum(soma(50))
print(s)
