arr = [1,2,3,4,5,6,7,8]
# arr = [1,3,7,11,12,14,18]

n = len(arr)
max_len = 0
dp = [[2 for _ in range(n)] for _ in range(n)]
for i in range(n):
    dp[i][0] = 0

map_k = {}
for idx, val in enumerate(arr):
    map_k[val] = idx

for i in range(n-2):
    for j in range(i+1, n-1):
        if arr[i] + arr[j] in map_k:
            k = map_k[arr[i] + arr[j]]
            dp[j][k] = max(dp[j][k], dp[i][j] + 1)
            max_len = max(max_len, dp[j][k])

print(max_len)

