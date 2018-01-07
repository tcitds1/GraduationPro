def printarr(arr):
    val = ''
    for i in arr:
            val += str(i) + ' '
    print(val)

l = range(10)

printarr(l)
printarr(l[::2])
printarr(l[::-2])

#从下标0开始，以2为步长
