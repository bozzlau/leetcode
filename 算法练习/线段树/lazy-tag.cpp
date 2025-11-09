//洛谷P3372 线段树lazy-tag
#include <iostream>
using namespace std;

#define ll long long
const ll NN = 1e5+1;
ll a[NN], tree[NN*4], tag[NN*4];

ll ls(ll p){return p << 1;}
ll rs(ll p){return p << 1 | 1;}

void pushUp(ll p){
    tree[p] = tree[ls(p)] + tree[rs(p)];
}
void build(ll p, ll pl, ll pr){
    if (pl == pr) {tree[p] = a[pl]; return;}
    
    ll mid = pl + (pr-pl) / 2;
    build(ls(p), pl, mid);
    build(rs(p), mid+1, pr);
    pushUp(p);
}

void addEleTag(ll p, ll pl, ll pr, ll d){
    tree[p] += (pr-pl+1) * d;
    tag[p] += d;
}

void pushDown(ll p, ll pl, ll pr){
    if (tag[p]){
        ll mid = pl + (pr-pl) / 2;
        addEleTag(ls(p), pl, mid, tag[p]);
        addEleTag(rs(p), mid+1, pr, tag[p]);
        tag[p] = 0;
    }
}

void update(ll p, ll pl, ll pr, ll L, ll R, ll d){
    if (L <= pl && pr <= R){
        addEleTag(p, pl, pr, d);
        // tree[p] += (pr-pl+1) * d;
        // tag[p] += d;
        return;
    }

    pushDown(p, pl, pr);
    ll mid = pl + (pr-pl) / 2;
    if (L <= mid) update(ls(p), pl, mid, L, R, d);
    if (R > mid) update(rs(p), mid+1, pr, L, R, d);
    pushUp(p);
}

ll query(ll p, ll pl, ll pr, ll L, ll R){
    if (L <= pl && pr <= R) return tree[p];

    pushDown(p, pl, pr);//把修改tag向下传递
    ll mid = pl + (pr-pl) / 2;
    ll ans = 0;
    if (L <= mid) ans += query(ls(p), pl, mid, L, R);
    if (R > mid) ans += query(rs(p), mid+1, pr, L, R);
    return ans;
}

int main(){
    int n, m;
    scanf("%d%d", &n, &m);
    for (ll i = 1; i <= n; i++) scanf("%lld", &a[i]);
    
    build(1, 1, n);
    while (m--){
        int op; scanf("%d", &op);
        int x, y;
        ll k;
        if (op == 1){
            scanf("%d%d%lld", &x, &y, &k);
            update(1, 1, n, x, y, k);
        }else{
            scanf("%d%d", &x, &y);
            printf("%lld\n", query(1, 1, n, x, y));
        }
    }
}