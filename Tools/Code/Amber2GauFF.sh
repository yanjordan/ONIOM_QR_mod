#!/bin/bash



grep '^[A-Z0-9][A-Za-z0-9\* ] [ ]*[0-9][0-9]*\.[0-9]*' parm96.dat > atom.tmp

grep '^[A-Z0-9][A-Za-z0-9\* ]-[A-Z0-9][A-Za-z0-9\* ] [ ]*[0-9][0-9]*\.[0-9]* [ ]*[0-9][0-9]*\.[0-9]*' parm96.dat > bond.tmp

grep '^[A-Z0-9][A-Za-z0-9\* ]-[A-Z0-9][A-Za-z0-9\* ]-[A-Z0-9][A-Za-z0-9\* ] [ ]*[0-9][0-9]*\.[0-9]* [ ]*[0-9][0-9]*\.[0-9]*' parm96.dat > angle.tmp

grep '^[A-Z0-9][A-Za-z0-9\* ]-[A-Z0-9][A-Za-z0-9\* ]-[A-Z0-9][A-Za-z0-9\* ]-[A-Z0-9][A-Za-z0-9\* ] [ ]*[0-9] [ ]*[0-9][0-9]*\.[0-9]* [ ]*[0-9][0-9]*\.[0-9]* [ ]*[0-9\-][0-9]*\.[0-9]*' parm96.dat > dihe.tmp

grep '^[A-Z0-9][A-Za-z0-9\* ]-[A-Z0-9][A-Za-z0-9\* ]-[A-Z0-9][A-Za-z0-9\* ]-[A-Z0-9][A-Za-z0-9\* ] [ ]*[0-9][0-9]*\.[0-9]* [ ]*[0-9][0-9]*\.[0-9]* [ ]*[0-9\-][0-9]*\.[0-9]*' parm96.dat > impr.tmp

grep '^  [A-Z0-9][A-Za-z0-9\* ] [ ]*[0-9][0-9]*\.[0-9]* [ ]*[0-9][0-9]*\.[0-9]*' parm96.dat > vdw.tmp


