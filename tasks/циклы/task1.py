import random

arr=[random.randint(1,100) for i in range(6)]
res=[-1,-1,None]
print(arr)
for i in range(len(arr)):
    if res[0]<1:
        res[0]=i
    else:
        if res[1]==-1:
            res[1]==i
            res[2]=arr[i-1]+arr[i]
        else:
            if arr[i-1]+arr[i]<res[2]:
                res[0]=i-1
                res[1]=i
                res[2]=arr[i-1]+arr[i]
print(res)
