#!/usr/bin/python3

import os
import argparse
import subprocess
import nibabel as nib
from nilearn.image import crop_img, load_img

parser = argparse.ArgumentParser()
parser.add_argument('-inpath', required=True, type=str, help='Path to the input NIfTI file')
parser.add_argument('-outdir', required=True, type=str, help='Output directory for the cropped file')
parser.add_argument('-filename', required=True, type=str, help='Output filename for the cropped file')
parser.add_argument('-rtol', type=float, default=0.01, help='Relative tolerance for nilearn cropping (default: 0.01)')

args = parser.parse_args()

inpath = args.inpath
outdir = args.outdir
filename = args.filename
rtol = args.rtol

# Ensure output directory exists
os.makedirs(outdir, exist_ok=True)

# Step 1: Run FSL's robustfov to perform initial cropping
robustfov_output = os.path.join(outdir, "robustfov_" + filename)
robustfov_cmd = f"robustfov -i {inpath} -r {robustfov_output}"
print(f"Running: {robustfov_cmd}")
subprocess.run(robustfov_cmd, shell=True, check=True)

# Step 2: Load robustfov output and apply nilearn's crop_img with rtol
print(f"Applying nilearn cropping with rtol={rtol}...")
robustfov_img = load_img(robustfov_output)
cropped_img = crop_img(robustfov_img, rtol=rtol)

# Step 3: Save the final cropped image
final_output_path = os.path.join(outdir, filename)
cropped_img.to_filename(final_output_path)

# Step 4: Clean up intermediate robustfov file
os.remove(robustfov_output)
print(f"Deleted intermediate file: {robustfov_output}")

print(f"Final cropped file saved to: {final_output_path}")
