pow2m1 = []
for i in range(1, 11):
    pow2m1.append(i ** 2 - 1)
print(pow2m1)

pow2m1 = [i**2-1 for i in range(1,11)]
print(pow2m1)

pow2m1 = list(map(lambda i: i**2-1,range(1,11)))
print(pow2m1)
