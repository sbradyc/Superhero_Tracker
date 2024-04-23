@echo off

set TESTS=("db_tests.py")
for %%t in %TESTS% do (
    python %%t
    if errorlevel 1 (
	echo [31m[-] %%t FAILED![0m
        exit /b 1
    ) else (
	echo [32m[+] %%t PASSED![0m
    )
)
echo [32m[+] ALL TESTS PASSED![0m
