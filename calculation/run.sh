#!/bin/bash

COUNT=1

forpython3

until [ $COUNT -gt 5 ]; do
    python cal_cor.py $COUNT
    python xi2dTOxiLegendre_Cmu_spline.py xi2d/xi2d-$COUNT.txt
    python plot_corr.py $COUNT
    let COUNT=COUNT+1
done
