#!/bin/bash

COUNT=1

until [ $COUNT -gt 600 ]; do
    python cal_cor.py $COUNT
    python xi2dTOxiLegendre_Cmu_spline.py xi2d/xi2d-$COUNT.txt
    python plot_corr.py $COUNT
    echo ************FINISHED FILE $COUNT**********
    let COUNT=COUNT+1
done
