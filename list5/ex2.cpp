#include <iostream>
#include "field.cpp"
#include <tuple>
#include <cassert>
#include <fstream>

using namespace std;

mpz_t modulo;
mpz_class d = -376014;
typedef Field<modulo> Number;
typedef pair<Number,Number> Point;

Point edwardsAdd(const Point firstPoint, const Point secondPoint) {
    auto [x1, y1] = firstPoint;
    auto [x2, y2] = secondPoint;
    Number x = (x1 * y2 + x2 * y1) / (Number(1) + Number(d) * x1 * x2 * y1 * y2);
    Number y = (y1 * y2 - x1 * x2) / ( Number(1) - Number(d) * x1 * x2 * y1 * y2);
    return make_pair(x,y);
}

Point scalarMulti(mpz_class scalar, Point P) {
    if (scalar == 0) {
        return make_pair(Number(0),Number(1));
    }
    if (scalar == 1) {
        return P;
    }
    Point Q = scalarMulti(scalar / 2, P);
    Q = edwardsAdd(Q,Q);
    if ((scalar & 1) == 1) {
        Q = edwardsAdd(P,Q);
    }
    return Q;
}

bool isOnCurve(Point point) {
    auto [x, y] = point;
    Number test = x * x + y * y - Number(1) - Number(d) * x * x * y * y;
    if (test == Number(0)) {
        return true;
    }
    return false;
}

void printPoint(Point point) {
    cout << point.first.getValue() << " " << point.second.getValue() << endl;
}


void setupModulo() {
    mpz_ui_pow_ui(modulo, 2, 521);
    mpz_sub_ui(modulo, modulo, 1);
}

unsigned long long int getSeed() {
    unsigned long long int seed;
    ifstream random("/dev/random", ios::in|ios::binary);
    random.read(reinterpret_cast<char*>(&seed), sizeof(seed));
    return seed;
}

Point createGenerator() {
    Number y = Number(12);
    mpz_class xn;
    xn = "15710548941849953875359397498943175686452973504 \
    02905821437625181152304994381188529632591196067604100772673927915114267193389905003276673749012051148356041324";
    Number x = Number(xn);
    return make_pair(x, y);
}

tuple<mpz_class, Point> generateKeys(gmp_randclass& rand, Point generator) {
    mpz_class a = rand.get_z_range(mpz_class(modulo)); // Private key a (integer)
    Point A = scalarMulti(a, generator); // Public key R (a * P), point on EC
    return make_tuple(a, A);
}

tuple<Point, Point> encrypt(Point message, Point generator, Point pubKey, gmp_randclass& rand) {
    mpz_class k = rand.get_z_range(mpz_class(modulo));
    Point Q = scalarMulti(k, generator); // Q = (k * p), point on EC
    Point kR = scalarMulti(k, pubKey);	// k * R = (k(aP)), point on EC
    Point crypto = edwardsAdd(message, kR); // crypto = M + kR
    return make_tuple(Q, crypto);
}

Point decrypt(Point Q, Point crypto, mpz_class privKey) {
    Point aQ = scalarMulti(privKey, Q); // a * Q = (a(kP)), point on EC
    Point minus_aQ = make_pair(-aQ.first, aQ.second); // M = crypto + (-aQ) (-aQ = {-x,y})
    return edwardsAdd(minus_aQ, crypto);
}

int main(int argc, char const *argv[]) {
    setupModulo();
    gmp_randclass r(gmp_randinit_default);
    r.seed(getSeed());
    Point generator = createGenerator();
    auto [privKey, pubKey] = generateKeys(r, generator);
    mpz_class scalarMessage = r.get_z_range(mpz_class(modulo));
    Point pointMessage = scalarMulti(scalarMessage, generator);
    cout << "MESSAGE" << endl;
    printPoint(pointMessage);
    auto [Q, crypto] = encrypt(pointMessage, generator, pubKey, r);
    cout << endl << "CRYPTO" << endl;
    printPoint(crypto);
    Point decMessage = decrypt(Q, crypto, privKey);
    cout << endl << "DECRYPT" << endl;
    printPoint(decMessage);
    assert(pointMessage.first == decMessage.first && pointMessage.second == decMessage.second);
}
