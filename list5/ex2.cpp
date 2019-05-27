#include <iostream>
#include "field.cpp"
#include <fstream>

using namespace std;

mpz_t modulo;
mpz_class d;
mpz_class I;
typedef Field<modulo> Number;

pair<Number,Number> edwardsAdd(const pair<Number,Number> firstPoint, const pair<Number,Number> secondPoint) {
    Number x1 = firstPoint.first;
    Number y1 = firstPoint.second;
    Number x2 = secondPoint.first;
    Number y2 = secondPoint.second;
    Number x = (x1 * y2 + x2 * y1) / (Number(1) + Number(d) * x1 * x2 * y1 * y2);
    Number y = (y1 * y2 - x1 * x2) / ( Number(1) - Number(d) * x1 * x2 * y1 * y2);
    return make_pair(x,y);
}

pair<Number, Number> scalarMulti(mpz_class scalar, pair<Number,Number> P){
    if (scalar == 0){
        return make_pair(Number(0),Number(1));
    }
    if (scalar == 1){
        return P;
    }
    pair<Number, Number> Q = scalarMulti(scalar / 2, P);
    Q = edwardsAdd(Q,Q);
    if ((scalar & 1) == 1){
        Q = edwardsAdd(P,Q);
    }
    return Q;
}

bool isOnCurve(pair<Number, Number> point) {
    Number x = point.first;
    Number y = point.second;
    Number test = x * x + y*y - Number(1) - Number(d)*x*x*y*y;
    if (test == Number(0)){
        return true;
    }
    return false;
}

void printPoint(pair<Number, Number> point){
    cout << point.first.getValue() << " " << point.second.getValue() << endl;
}

Number xRecover(Number y) {
    Number xx = (y * y - Number(1)) / (Number(d) * y * y - Number(1));
    mpz_class x_tmp = xx.getValue();
    mpz_class exp_x(modulo);
    exp_x = (exp_x + 3) / 8;
    mpz_class test;
    mpz_powm(test.get_mpz_t(),x_tmp.get_mpz_t(),exp_x.get_mpz_t(), modulo);
    Number x(test);
    if ((x * x - xx) != Number(0)){
        x = x * Number(I);
    }
    if ((x % Number(2)) != 0) {
        x = Number(modulo) - x;
    }
    return x;
}

void setupModulo(){
    mpz_ui_pow_ui(modulo,2,255);
    mpz_sub_ui(modulo,modulo,19);
}
void setupDValue(){
    d = -121665;
    mpz_class tmp_2 = 121666;
    mpz_invert(tmp_2.get_mpz_t(),tmp_2.get_mpz_t(),modulo);
    d *= tmp_2;
}

void setupIValue(){
    mpz_class tmp_i = 2;
    mpz_class exp_i(modulo);
    exp_i = (exp_i - 1) / 4;
    mpz_powm(I.get_mpz_t(),tmp_i.get_mpz_t(),exp_i.get_mpz_t(), modulo);
}

pair<Number, Number> createGenerator() {
    Number by = Number(4) / Number(5);
    Number bx = xRecover(by);
    return make_pair(bx, by);
}


int main(int argc, char const *argv[]) {
    setupModulo();
    setupDValue();
    setupIValue();
    pair<Number, Number> P = createGenerator();

    gmp_randclass r(gmp_randinit_default);
    unsigned long long int seed = 0;
    ifstream urandom("/dev/urandom", ios::in|ios::binary);
    urandom.read(reinterpret_cast<char*>(&seed), sizeof(seed));
    r.seed(seed);

    mpz_class a = r.get_z_range(mpz_class(modulo)); // Private key a (integer)
    pair<Number, Number> R = scalarMulti(a, P); // Public key R (a * P), point on EC
    // ---------------------------------- ENC -------------------------
    mpz_class k = r.get_z_range(mpz_class(modulo));
    pair<Number, Number> Q = scalarMulti(k, P);
    pair<Number, Number> kR = scalarMulti(k,R);
    mpz_class message;
    Number x_message;
    pair <Number, Number> p_message;
    do {
        message = r.get_z_range(mpz_class(modulo));
        x_message = xRecover(Number(message));
        p_message = make_pair(x_message, message);
    }
    while(!isOnCurve(p_message));
    cout << "MESSAGE" << endl;
    printPoint(p_message);
    pair<Number, Number> crypto = edwardsAdd(p_message, kR);
    cout << "CRYPTO" << endl;
    printPoint(crypto);
    // ---------------------------------- DEC-------------------------
    pair<Number, Number> aQ = scalarMulti(a, Q);
    pair<Number, Number> dec_aQ = make_pair(-aQ.first,aQ.second);
    pair <Number, Number> dec_m = edwardsAdd(dec_aQ, crypto);
    printPoint(dec_m);

}
