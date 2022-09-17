import matplotlib.pyplot as plt
import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing.properties import Properties, LayoutProperties
from ezdxf.addons.drawing.config import Configuration
import re
import os
import argparse
import io

# DXF
def parse_autocad(path, output_path):
    # https://stackoverflow.com/questions/58906149/python-converting-dxf-files-to-pdf-or-png-or-jpeg
    print("parsing autocad")

    doc = ezdxf.readfile(path)
    msp = doc.modelspace()
    # Recommended: audit & repair DXF document before rendering
    auditor = doc.audit()
    # The auditor.errors attribute stores severe errors,
    # which *may* raise exceptions when rendering.
    if len(auditor.errors) != 0:
        raise Exception("The DXF document is damaged and can't be converted!")
    else :
        fig = plt.figure()
        ctx = RenderContext(doc)
        # Better control over the LayoutProperties used by the drawing frontend
        layout_properties = LayoutProperties.from_layout(msp)
        layout_properties.set_colors(bg='#000000')
        ax = fig.add_axes([0, 0, 1, 1])
        out = MatplotlibBackend(ax)
        config = Configuration.defaults()
        config = config.with_changes(lineweight_scaling=0, min_lineweight=0.02, hatch_policy="SHOW_SOLID")
        Frontend(ctx, out, config=config).draw_layout(msp, layout_properties=layout_properties, finalize=True)
        buffer = io.StringIO()
        fig.savefig(buffer, format="svg") # save to ram
        svg_fill(buffer, output_path) # read from ram and write to disk

def svg_fill(buffer, output_path): # fill polylines in svg for visibility improvement
    lines = []
    buffer.seek(0)
    lines = buffer.read()
    lines = lines.split("\n")
    for count in range(len(lines)):
        matches = re.search(r"; stroke:(.*?);", lines[count])
        if matches is not None:
            color = matches.groups()[0]
            lines[count] = re.sub(r'fill:(.*?);', fr'fill:{color};', lines[count]) # add fill color
            lines[count] = re.sub(r'fill:', fr'fill-opacity=50%;fill:', lines[count]) # add fill opacity

    with open(output_path, "w") as f:
        f.writelines(line+"\n" for line in lines)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="input path")
    args = parser.parse_args()
    input_path = args.path
    input_directory = os.path.dirname(input_path)
    input_filename = os.path.basename(input_path)
    input_filename_wo_ext = os.path.splitext(input_filename)[0]

    output_directory = os.path.join(input_directory, "report")
    output_filename = input_filename_wo_ext + ".svg"
    output_path = os.path.join(output_directory, output_filename)
    if not os.path.isdir(output_directory):
        os.mkdir(output_directory)
    parse_autocad(input_path, output_path)