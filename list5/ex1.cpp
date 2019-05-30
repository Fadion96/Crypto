#include <iostream>
#include "field.cpp"
#include <cassert>

using namespace std;

mpz_t modulo;
mpz_class d;

typedef Field<modulo> Number;
typedef pair<Number,Number> Point;

Point edwardsAdd(const Point firstPoint, const Point secondPoint) {
    auto [x1, y1] = firstPoint;
    auto [x2, y2] = secondPoint;
    Number x = (x1 * y2 + x2 * y1) / (Number(1) + Number(d) * x1 * x2 * y1 * y2);
    Number y = (y1 * y2 - x1 * x2) / ( Number(1) - Number(d) * x1 * x2 * y1 * y2);
    return make_pair(x,y);
}

void initModulo(long long value) {
    mpz_init_set_ui(modulo, value);
}

void printPoint(Point point) {
    cout << point.first.getValue() << " " << point.second.getValue() << endl;
}

int main(int argc, char const *argv[]) {
    initModulo(1009);
    d = -11;
    Point P1 = make_pair(Number(7), Number(415));
    Point P2 = make_pair(Number(23), Number(487));
    Point output = edwardsAdd(P1,P2);
    printPoint(output);
    assert(output.first == 944 && output.second == 175);
    output = edwardsAdd(P2,P1);
    assert(output.first == 944 && output.second == 175);
}
