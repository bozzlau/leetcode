arr = [1,2,3,4,5,6,7,8]
# arr = [1,3,7,11,12,14,18]

i, j, k = 0, 1, 2
n = len(arr)
max_len = 0

map_k = {}
for idx, val in enumerate(arr):
    map_k[val] = idx

for i in range(n-2):
    res = [arr[i]]
    for j in range(i+1, n-1):
        is_fib = False
        ti = i; tj = j
        res.append(arr[j])

        while arr[ti] + arr[tj] in map_k:
            is_fib = True
            tk = map_k[arr[ti] + arr[tj]]
            res.append(arr[tk])
            ti, tj = tj, tk
            max_len = max(max_len, len(res))
        
        if is_fib: print(res)
        for _ in range(len(res)-1):
            res.pop()
        # for k in range(j+1, n):
        #     tk = k
        #     if arr[ti] + arr[tj] == arr[tk]:
        #         is_fib = True
        #         ti, tj = tj, tk
        #         res.append(arr[tk])
        #         max_len = max(max_len, len(res))
print(max_len)

