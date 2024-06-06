#!/bin/bash

rm -Rf ./allure-report
pytest -s -v ./ --alluredir=./allure-report
allure serve ./allure-report