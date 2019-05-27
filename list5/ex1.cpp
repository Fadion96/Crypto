#include <iostream>
#include "field.cpp"
#include <cassert>

using namespace std;

mpz_t modulo;
mpz_class d;

typedef Field<modulo> Number;

void initModulo(long long value){
    mpz_init_set_ui(modulo, value);
}

pair<Number,Number> edwardsAdd(const pair<Number,Number> first, const pair<Number,Number> second) {
    Number x1 = first.first;
    Number y1 = first.second;
    Number x2 = second.first;
    Number y2 = second.second;
    Number x = (x1 * y2 + y1 * x2) / (Number(1) + Number(d) * x1 * y1 * x2 * y2);
    Number y = (y1 * y2 - x1 * x2) / (Number(1) - Number(d) * x1 * y1 * x2 * y2);
    return make_pair(x,y);
}

void printPoint(pair<Number, Number> point){
    cout << point.first.getValue() << " " << point.second.getValue() << endl;
}

int main(int argc, char const *argv[]) {
    initModulo(1009);
    d = -11;
    pair<Number,Number> P1 = make_pair(Number(7), Number(415));
    pair<Number,Number> P2 = make_pair(Number(23), Number(487));
    pair<Number,Number> output = edwardsAdd(P1,P2);
    printPoint(output);
    assert(output.first == 944 && output.second == 175);
    output = edwardsAdd(P2,P1);
    assert(output.first == 944 && output.second == 175);
    // pair<Number,Number> test = make_pair(-Number(7), Number(415));
    // printPoint(test);
    // pair<Number,Number> inv = edwardsAdd(output,test);
    // printPoint(inv);

}
