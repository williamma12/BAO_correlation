#!/bin/bash

COUNTER=1

mkdir result

until [ $COUNTER -gt 5 ]; do
    touch result/result_south_$COUNTER-DD.dat
    touch result/result_south_$COUNTER-DR.dat
    touch result/result_south_$COUNTER-RR.dat
    touch result/result_south_$COUNTER-norm.dat
    let COUNTER=COUNTER+1
done
