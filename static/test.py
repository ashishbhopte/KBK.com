
#1,2,2,3,4,5,5,3

l=[1,2,2,3,4,5,5,3]
l1=[]
for i in range(len(l)-1):
    if l[i]==l[i+1]:
        l1.append(i)
        l1.append(i+1)
print(l1)
count=0
for i in l1:
    print(l)
    l.pop(i-count)
    count+=1
print(l)

