a = ['1992-03-13','1992-03-14','1992-03-11','1992-03-01']
b = {}
d = []
for i in sorted(a):
    for c in [1,2,3]:
        d.append(c)
    b[i] = d
print b

