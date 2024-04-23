#!/bin/bash

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'
TESTS=("db_tests.py")
for test in ${TESTS[@]}; do
    python ${test}
    if [ $? -ne 0 ]; then
        echo -e "${RED}[-] ${test} FAILED!${NC}"
        exit 1
    else
        echo -e "${GREEN}[+] ${test} PASSED!${NC}"
    fi
done
echo -e "${GREEN}[+] ALL TESTS PASSED!${NC}"
