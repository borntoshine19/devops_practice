#!/bin/bash

echo "начало скрипта"

mycomputer "lenovo"
myOS=`uname -a`

echo "Этот скрипт $1"
echo "Второе значение = $2"

num1=50
num2=111
summa=$((num1+num2))

echo "$num1 + $num2 = $summa"
