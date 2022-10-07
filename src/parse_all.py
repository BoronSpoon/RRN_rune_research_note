# profilometer
import numpy as np
import argparse, os, sys, io
import parse_dxf
import parse_oscilloscope
import parse_profilometer
import parse_vsm
from misc import *
#import parse_pptx

def read_files(**kwargs):
    with open(kwargs["input_path"], "r") as f:
        lines = f.readlines()

    if ".txt" in kwargs["input_filename"] or ".TXT" in kwargs["input_filename"]: # profilometer
        parse_profilometer.main(**kwargs)
    elif ".Dat" in kwargs["input_filename"]: # VSM
        parse_vsm.main(**kwargs)
    #elif ".pptx" in filename or ".PPTX" in filename: # pptx
    #    parse_pptx.main(**kwargs)
    elif ".dxf" in kwargs["input_filename"] or ".DXF" in kwargs["input_filename"]: # autocad DXF
        parse_dxf.main(**kwargs)
    elif "DL9000" in lines[1]: # oscilloscope_electrical
        parse_oscilloscope.main(**kwargs)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="input path")
    args = parser.parse_args()
    input_path = args.path
    input_directory = os.path.dirname(input_path)
    input_filename = os.path.basename(input_path)
    input_filename_wo_ext = os.path.splitext(input_filename)[0]

    output_directory = os.path.join(input_directory, "report")
    output_filename_wo_ext = input_filename_wo_ext
    output_filename = output_filename_wo_ext + ".svg"
    output_path = os.path.join(output_directory, output_filename)
    if not os.path.isdir(output_directory):
        os.mkdir(output_directory)
    read_files(**{
        "input_path": input_path,
        "input_directory": input_directory,
        "input_filename": input_filename,
        "input_filename_wo_ext": input_filename_wo_ext,
        "output_path": output_path,
        "output_directory": output_directory,
        "output_filename": output_filename,
        "output_filename_wo_ext": output_filename_wo_ext,
    })