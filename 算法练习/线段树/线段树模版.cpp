#include <iostream>
#include <algorithm>
using namespace std;
const int MAXN = 1e5+1;
int a[MAXN];
int tree[MAXN*4];

int ls(int p){return 2*p;}
int rs(int p){return 2*p+1;}

void pushUp(int p){
    // tree[p] = tree[ls(p)] + tree[rs(p)];
    // tree[p] = tree[ls(p)] > tree[rs(p)] ? tree[rs(p)] : tree[ls(p)];
    tree[p] = min(tree[ls(p)], tree[rs(p)]);
}

void build(int p, int pl, int pr){
    if (pl == pr){
        tree[p] = a[pl]; return;
    }

    int mid = pl + (pr-pl) / 2;
    build(ls(p), pl, mid);
    build(rs(p), mid+1, pr);
    pushUp(p);
}

int query(int p, int pl, int pr, int L, int R){
    if (L <= pl && pr <= R) return tree[p];
    int mid = pl + (pr-pl) / 2;
    int ans = 100001;
    // if (L <= mid) ans += query(ls(p), pl, mid, L, R);
    // if (R > mid) ans += query(rs(p), mid+1, pr, L, R);
    if (L <= mid) ans = min(ans, query(ls(p), pl, mid, L, R));
    if (R > mid) ans = min(ans, query(rs(p), mid+1, pr, L, R));
    return ans;
}
int main(){
    int m, n;
    scanf("%d%d", &m, &n);
    for (int i = 1; i <= m; i++) scanf("%d", &a[i]);
    
    build(1, 1, m);
    for (int i = 0; i < n; i++){
        int a, b;
        scanf("%d%d", &a, &b);
        printf("%d ", query(1, 1, m, a, b));
    }

    return 0;
}