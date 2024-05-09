import itertools

n = "ПАЛИНДРОМ"
perm_set = itertools.permutations(n)

for i in perm_set:
    print(i)
