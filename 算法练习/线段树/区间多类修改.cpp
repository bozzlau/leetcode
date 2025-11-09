#include <iostream>
using namespace std;

#define ll long long
const int NN = 1e5+1;
ll a[NN], tree[NN*4], add_tag[NN*4], mul_tag[NN*4];
int mod;

int ls(int p){return p*2;}
int rs(int p){return p*2+1;}

void pushUp(int p){
    tree[p] = (tree[ls(p)] + tree[rs(p)]) % mod;
}

void build(int p, int pl, int pr){
    if (pl == pr){tree[p] = a[pl] % mod; return;}
    int mid = pl + (pr-pl) / 2;
    build(ls(p), pl, mid);
    build(rs(p), mid+1, pr);
    pushUp(p);
    mul_tag[p] = 1; //mul_tag初始化为1， add_tag初始化为0，全局变量默认已是0
}

void addEleTag(int p, int pl, int pr){
    int fp = p >> 1; //父节点
    tree[p] = (tree[p] * mul_tag[fp] + (pr-pl+1) * add_tag[fp]) % mod;
    mul_tag[p] = (mul_tag[p] * mul_tag[fp]) % mod;
    add_tag[p] = (add_tag[p] * mul_tag[fp] + add_tag[fp]) % mod;
}
void pushDown(int p, int pl, int pr){
    int mid = pl + (pr-pl) / 2;

    if (mul_tag[p] != 1 || add_tag[p] != 0){
        //下沉左子树
        addEleTag(ls(p), pl, mid);
        //下沉右子树
        addEleTag(rs(p), mid+1, pr);
        //下沉后父节点不再有更改记录标记
        mul_tag[p] = 1; add_tag[p] = 0;
    }

}
void updateMul(int p, int pl, int pr, int L, int R, int k){
    if (L <= pl && pr <= R){
        tree[p] = (tree[p] * k) % mod;
        mul_tag[p] = (mul_tag[p] * k) % mod;
        add_tag[p] = (add_tag[p] * k) % mod;
        return;
    }

    pushDown(p, pl, pr);
    int mid = pl + (pr-pl) / 2;
    if (L <= mid) updateMul(ls(p), pl, mid, L, R, k);
    if (R > mid) updateMul(rs(p), mid+1, pr, L, R, k);
    pushUp(p);
}

void updateAdd(int p, int pl, int pr, int L, int R, int k){
    if (L <= pl && pr <= R){
        tree[p] = (tree[p] + (pr-pl+1) * k) % mod;
        add_tag[p] = (add_tag[p] + k) % mod;
        return;
    }
    
    pushDown(p, pl, pr);
    int mid = pl + (pr-pl) / 2;
    if (L <= mid) updateAdd(ls(p), pl, mid, L, R, k);
    if (R > mid) updateAdd(rs(p), mid+1, pr, L, R, k);
    pushUp(p);
}

ll query(int p, int pl, int pr, int L, int R){
    if (L <= pl && pr <= R) return tree[p];

    pushDown(p, pl, pr);
    int mid = pl + (pr-pl) / 2;
    ll ans = 0;
    if (L <= mid) ans = (ans + query(ls(p), pl, mid, L, R)) % mod;
    if (R > mid) ans = (ans + query(rs(p), mid+1, pr, L, R)) % mod;
    return ans;
}

int main(){
    int n, q;
    scanf("%d%d%d", &n, &q, &mod);

    for (int i = 1; i <= n; i++) scanf("%lld", &a[i]);
    build(1, 1, n);
    
    while (q--){
        int op, x, y, k;
        scanf("%d", &op);
        if (op == 1){
            scanf("%d%d%d", &x, &y, &k);
            updateMul(1, 1, n, x, y, k);
        }else if (op == 2){
            scanf("%d%d%d", &x, &y, &k);
            updateAdd(1, 1, n, x, y, k);
        }else{
            scanf("%d%d", &x, &y);
            cout << query(1, 1, n, x, y) << endl;

        }
    }
}