##!/usr/bin/env bash

openssl x509 -pubkey -noout -in cacertificate.pem > pubkey.pem;
RsaCtfTool/RsaCtfTool.py --publickey pubkey.pem --private > privkey.pem;
openssl dgst -md5 -sign privkey.pem -out grade_forge.sign grade_forge.txt
openssl dgst -md5 -verify pubkey.pem -signature grade_forge.sign grade_forge.txt;
