#include "gmpxx.h"

template<mpz_t mod>
class Field {
private:
    mpz_class value;
public:
    Field(){
        
    }

    Field(mpz_t value){
        mpz_init(this->value.get_mpz_t());
        mpz_mod(this->value.get_mpz_t(), value, mod);
    }
    Field(mpz_class value){
        mpz_init(this->value.get_mpz_t());
        mpz_mod(this->value.get_mpz_t(), value.get_mpz_t(), mod);
    }
    Field(int value){
        mpz_t tmp;
        mpz_init_set_si(tmp,value);
        mpz_init(this->value.get_mpz_t());
        mpz_mod(this->value.get_mpz_t(), tmp, mod);
    }
    Field(long long value){
        mpz_t tmp;
        mpz_init_set_si(tmp,value);
        mpz_init(this->value.get_mpz_t());
        mpz_mod(this->value.get_mpz_t(), tmp, mod);
    }
    void getValue(mpz_t ret){
        mpz_init_set (ret,this->value.get_mpz_t());
    }
    mpz_class getValue(){
        return this->value;
    }

    Field operator + (Field const &obj) {
        mpz_class tmp = value + obj.value;
        return Field(tmp.get_mpz_t());
    }

    Field operator - (Field const &obj) {
        mpz_class tmp = value - obj.value;
        return Field(tmp.get_mpz_t());
    }

    Field operator - () {
        mpz_class tmp = - value;
        return Field(tmp.get_mpz_t());
    }

    Field operator * (Field const &obj) {
        mpz_t tmp;
        mpz_init(tmp);
        mpz_mul(tmp,value.get_mpz_t(), obj.value.get_mpz_t());
        return Field(tmp);
    }

    Field operator / (Field const &obj) {
        mpz_t tmp;
        mpz_t exp;
        mpz_init(tmp);
        mpz_init_set(exp,mod);
        mpz_sub_ui(exp,exp,2);
        mpz_powm(tmp ,obj.value.get_mpz_t(),exp,mod);
        mpz_mul(tmp,value.get_mpz_t(), tmp);
        return Field(tmp);
    }

    Field operator % (Field const &obj) {
        mpz_class tmp;
        mpz_mod(tmp.get_mpz_t(),value.get_mpz_t(),obj.value.get_mpz_t());
        return Field(tmp.get_mpz_t());
    }

    bool operator == (Field const &rhs) {
        return mpz_cmp(value.get_mpz_t(),rhs.value.get_mpz_t()) == 0;
    }

    bool operator != (Field const &rhs) {
        return mpz_cmp(value.get_mpz_t(),rhs.value.get_mpz_t()) != 0;
    }
};
