##!/usr/bin/env bash

# openssl x509 -pubkey -noout -in cacertSec.pem > pubkey2.pem;
openssl dgst -md5 -sign privkey.pem -out grade_2.sign grade_2.txt
openssl dgst -md5 -verify pubkey.pem -signature grade_2.sign grade_2.txt;
openssl dgst -md5 -verify pubkey.pem -signature grade_2.sign grade_forged_2.txt;
