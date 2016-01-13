#!/usr/bin/env python
""" This script takes multiple patch folders and detect inter-folder clones.

Usage: script.py ccfx lang folder1 folder2 ...

These folders should be the Repertoire's top output folder.
For example:
~/RepertoireOutput/clones
~/RepertoireOutput/proj0
~/RepertoireOutput/repertoire

The topfolder should be ~/RepertoireOutput
"""

import sys
import os
from subprocess import call
from subprocess import Popen
from path_builder import PathBuilder
from output_parser import RepertoireOutput
from ccfx_input_conv import CCFXInputConverter
from ccfx_entrypoint import CCFXEntryPoint
from ccfx_output_conv import convert_ccfx_output
from path_builder import PathBuilder

lang = 'cxx'
proj = 'proj0'

# script starts from here
argv_len = len(sys.argv)
if(argv_len < 4):
    print('Usage: script.py ccfx lang folder1 folder2 ...')
    sys.exit(2)

# get the ccfx_input_new folder
input_folder = 'ccfx_input_new'
patch_dirs = []
for argv in sys.argv[2:]:
    ccfx_input_new = argv + os.sep + proj + os.sep + lang + os.sep + input_folder
    if(os.path.isdir(ccfx_input_new)):
        patch_dirs.append(ccfx_input_new)
    else:
        print('ERROR: ' + argv + ' is not a valid folder!')
        sys.exit(-1)

result_file = 'crossFileGroup-thread.ccfxd'
cmd = ccfx + ' d ' + lang + ' -dn ' + \
	' -dn '.join(patch_dirs) + \
	'-w f-w-g+ -b 40 -o ' + result_file + ' --threads=30'

print('CMD: ' + cmd)
# execute ccFinder to detect clones and accept stdout
p = Popen(cmd, shell=True)
stdout, stderr = p.communicate()
if stderr:
	print(stderr)
    sys.exit(2)

print('===========ccFinder Output=============')
print(stdout)
print('=========ccFinder Output ends==========')


"""
We convert ccfinder output file from here.
Repertoire converter is for single project only.
We need to define a new way to use multiple file groups
"""
# We will build a dictionary which contains all groups and their path_builders
# build path, delete folder if exists with force_clean
pb_dict = {}
for argv in sys.argv[2:]:
    pb_dict[argv] = PathBuilder(argv, force_clean = True)




output = convert_ccfx_output(self.pb, proj='proj0', lang='cxx', is_new=True)
rep_out_path = self.pb.getRepertoireOutputPath(lang, is_new)
suffix = '_old.txt'
if is_new:
    suffix = '_new.txt'
output.writeToFile(rep_out_path + lang + suffix)
self.progress('Repertoire filtering based on operation')


print "Processing successful!!"
return ('Processing successful', True)
