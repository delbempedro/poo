selected = set()
for i in range(1, 100):
    if i % 7 == 1:
        selected.add(i)
print(selected)

selected = set([i for i in range(1,100) if i%7==1])
print(selected)

selected = set(filter(lambda x: x%7==1, range(1,100)))
print(selected)

