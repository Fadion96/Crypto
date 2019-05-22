#include <iostream>
#include "field.cpp"

using namespace std;

mpz_t modulo;
mpz_class d;
mpz_class I;
typedef Field<modulo> Number;


pair<Number,Number> edwardsAdd(const pair<Number,Number> first, const pair<Number,Number> second) {
    Number x1 = first.first;
    Number y1 = first.second;
    Number x2 = second.first;
    Number y2 = second.second;
    Number x = (x1 * y2 + y1 * x2) / (Number(1) + Number(d) * x1 * y1 * x2 * y2);
    Number y = (y1 * y2 - x1 * x2) / (Number(1) - Number(d) * x1 * y1 * x2 * y2);
    return make_pair(x,y);
}

pair<Number, Number> scalarMulti(long long scalar, const pair<Number,Number> P){
    if (scalar == 0){
        return make_pair(Number(0),Number(1));
    }
    else if (scalar == 1){
        return P;
    }
    else{
        pair<Number, Number> Q = scalarMulti(scalar / 2, P);
        Q = edwardsAdd(Q,Q);
        if (scalar % 2 == 1){
            Q = edwardsAdd(Q,P);
        }
        return Q;
    }
}

void printPoint(pair<Number, Number> point){
    cout << point.first.getValue() << " " << point.second.getValue() << endl;
}

Number xRecover(Number y) {
    Number xx = (y * y - Number(1)) / (Number(d) * y * y + Number(1));
    mpz_class x_tmp = xx.getValue();
    mpz_class exp_i(modulo);
    exp_i = exp_i + 3;
    exp_i = exp_i / 8;
    mpz_class test;
    mpz_powm(test.get_mpz_t(),x_tmp.get_mpz_t(),exp_i.get_mpz_t(), modulo);
    Number x(test);
    if ((x * x - xx) != Number(0)){
        x = x * Number(I);
    }
    if ((x % Number(2)) != 0) {
        x = Number(modulo) - x;
    }
    return x;
}

int main(int argc, char const *argv[]) {
    mpz_ui_pow_ui(modulo,2,255);
    mpz_sub_ui(modulo,modulo,19);
    mpz_class tmp_d = -121665;
    mpz_class tmp_2 = 121666;
    mpz_invert(tmp_2.get_mpz_t(),tmp_2.get_mpz_t(),modulo);
    d = tmp_d * tmp_2;
    mpz_class tmp_i = 2;
    mpz_class exp_i(modulo);
    exp_i = exp_i - 1;
    exp_i = exp_i / 4;
    mpz_powm(I.get_mpz_t(),tmp_i.get_mpz_t(),exp_i.get_mpz_t(), modulo);
    Number by = Number(4) / Number(5);
    Number bx = xRecover(by);
    pair<Number, Number> generator = make_pair(bx, by);
    printPoint(generator);


    // pair<Number, Number> a = edwardsAdd(make_pair(Number(7),Number(415)), make_pair(Number(23), Number(487)));
    // pair<Number, Number> b = edwardsAdd(make_pair(Number(23),Number(487)), make_pair(Number(7), Number(415)));
    // cout << a.first.getValue() << " " << a.second.getValue() << endl;
    // cout << b.first.getValue() << " " << b.second.getValue() << endl;
    // pair<Number, Number> c = scalarMulti(5,b);
    // cout << c.first.getValue() << " " << c.second.getValue() << endl;

}
