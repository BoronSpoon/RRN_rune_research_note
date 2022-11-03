VERN: Very Easy Research Note

how to use
##########
* create the following two files on your location of choice (desktop may be a good place)
* drag and drop to-be processed files on the run_vern.py

run_vern.bat
============

.. code-block:: bat

    cd %~dp0
    :loop
    if not "%~nx1"=="" (
    python run_vern.py %~f1 & shift & goto loop
    )
    pause

run_vern.py
===========

.. code-block:: python

    from vern import *
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    Vern(args.path)

contribute
##########

bug report
==========
Use the `issues` feature of GitHub. Please use only English

code update
===========
Use the `pull request` feature of GitHub. Please use only English

types of files
##############

profilometer (Tencor P7)
========================
* `*.txt` file will be regarded as a profilometer file
* modify filename to `*_i.txt` to enable interactive mode
    * interactive mode can crop part of the profile and apply it to normal plot and histogram

tabular
=======
* `*_m1.txt` file will be regarded as a tabular file
* tabular data is consisted of two columns
    * each column will be used as x and y data
    * the column labels will be used for the x and y axis label
    * x,y plot will be shown as dots
    * a linear approximation line will be added to the plot
        * the equations for the approximated line and the R2 value will appear on the plot

VSM
===
* in progress

oscilloscope
============
* in progress

dxf
===
* in progress
