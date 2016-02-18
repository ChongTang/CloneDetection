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
from output_parser import RepertoireOutput

lang = 'cxx'
proj = 'proj0'

class CCFXMetaData:
    # this is a little complex, so we're writing a nice comment about it
    # 1. we start with big aggregate diff files between versions
    # 2. we then filter those big diff files by language in files like 0027.c
    # 3. ccfx needs c-ish looking input, so we remove the diff metadata
    # 4. we save a mapping between lines in the diff and lines in the ccfx input
    # 5. ccfx processes the file, spitting out a metadata file per input file
    # 6. we use the metadata file, the output from ccfx, and our own mapping
    #    to build a datastructure that saves how lines in different diffs (2)
    #    are clones of other lines in other diffs (2)
    #
    # ccfx_input        == path to a file from 3
    # ccfx_preprocessed == path to a file from 5
    # filter_conv       == path to a file from 4
    # fitler_output     == path to a file from 2
    def __init__(self, base_path, ccfx_input, ccfx_preprocessed, filter_conv, filter_output):
        self.basePath = base_path
        self.ccfxInput = ccfx_input
        self.ccfxPrep  = ccfx_preprocessed
        self.filterConv = filter_conv
        self.filterOutput = filter_output

class CCFXMetaMapping:
    def __init__(self):
        self.name2meta = {}

    def addFile(self, meta):
        self.name2meta[meta.ccfxInput] = meta

    def getMetas(self):
        return self.name2meta.values()

    def getMetaForPath(self, input_path):
        return self.name2meta.get(input_path, None)

    def hasInputPath(self, input_path):
        return not self.getMetaForPath(input_path) is None

'''
filter_path = /if7/ct4ew/research/ray/project/src/repertoire/tmp_data/linux2012_patch/proj0/cxx/filter_output/
conv_path = /if7/ct4ew/research/ray/project/src/repertoire/tmp_data/linux2012_patch/proj0/cxx/ccfx_mappings_new/
ccfx_i_path = /if7/ct4ew/research/ray/project/src/repertoire/tmp_data/linux2012_patch/proj0/cxx/ccfx_input_new/
ccfx_p_path = /if7/ct4ew/research/ray/project/src/repertoire/tmp_data/linux2012_patch/proj0/cxx/ccfx_input_new/.ccfxprepdir/
'''
def check_path_exists(path):
    if not os.path.exists(path):
        print 'Path does not exist: ', path
        sys.exit(-1)
    return True

def getFilterOutputPath(file_group):
    path = os.path.join(file_group, proj, lang, 'filter_output'+os.sep)
    check_path_exists(path)
    return path

def getLineMapPath(file_group):
    path = os.path.join(file_group, proj, lang, 'ccfx_mappings_new'+os.sep)
    check_path_exists(path)
    return path

def getCCFXInputPath(file_group):
    path = os.path.join(file_group, proj, lang, 'ccfx_input_new'+os.sep)
    check_path_exists(path)
    return path

def getCCXFPrepPath(file_group):
    path = os.path.join(file_group, proj, lang, 'ccfx_input_new', '.ccfxprepdir'+os.sep)
    check_path_exists(path)
    return path

def getCCFXOutputPath(file_group):
    path = os.path.join(file_group, 'clones' + os.sep)
    check_path_exists(path)
    return path

# the output of the ccfx prep scripts are a little funny,
# find the ccfx prep file in path (a directory) for file name (no path)
# ie self.findPrepFile('/home/user/myworkdir/more/.ccfxprepdir/', '0027.c')
def findPrepFileFor(path, name):
    for f in os.listdir(path):
        if f.startswith(name):
            return f
    raise Exception("Couldn't find prep file for diff with name: {0}".format(name))

def makeLineMapFileName(old_name):
    return old_name.partition('.')[0] + '.conv'

def getCCFXOutputFileName(lang, is_new, is_tmp):
    if is_new:
        ext = '_new'
    else:
        ext = '_old'

    if is_tmp:
        ext = ext + '.ccfxd'
    else:
        ext = ext + '.txt'
    return lang + ext
groups = ['/if7/ct4ew/research/ray/project/src/repertoire/tmp_data/linux2007_patch',
            '/if7/ct4ew/research/ray/project/src/repertoire/tmp_data/linux2008_patch',
            '/if7/ct4ew/research/ray/project/src/repertoire/tmp_data/linux2009_patch',
            '/if7/ct4ew/research/ray/project/src/repertoire/tmp_data/linux2010_patch',
            '/if7/ct4ew/research/ray/project/src/repertoire/tmp_data/linux2011_patch',
            '/if7/ct4ew/research/ray/project/src/repertoire/tmp_data/linux2012_patch',
            '/if7/ct4ew/research/ray/project/src/repertoire/tmp_data/linux2013_patch',
            '/if7/ct4ew/research/ray/project/src/repertoire/tmp_data/linux2014_patch',
            '/if7/ct4ew/research/ray/project/src/repertoire/tmp_data/linux2015_patch']
#groups = ['/if7/ct4ew/research/ray/project/src/repertoire/tmp_data/linux2007_patch']
# get filter paths
metaDB = CCFXMetaMapping()

for folder in groups:
    filter_path = getFilterOutputPath(folder)
    conv_path   = getLineMapPath(folder)
    ccfx_i_path = getCCFXInputPath(folder)
    ccfx_p_path = getCCXFPrepPath(folder)
    for name in os.listdir(filter_path):
        meta = CCFXMetaData(
            folder,
            ccfx_i_path + name,
            ccfx_p_path + findPrepFileFor(ccfx_p_path, name),
            conv_path + makeLineMapFileName(name),
            filter_path + name)
        metaDB.addFile(meta)

print 'metaDB length: ', len(metaDB.name2meta)

# we have our files, now map line numbers in the prep files to input files
for meta in metaDB.getMetas():
    prepHandler = open(meta.ccfxPrep, 'r')
    prep = prepHandler.readlines()
    prepHandler.close()

    convHandler = open(meta.filterConv, 'r')
    conv = convHandler.readlines()
    convHandler.close()

    input2orig = {}
    pidx2orig = {}
    origline2op = {}
    # build a map of line numbers in ccfx_input to filtered diff line
    for i, cline in enumerate(conv):
        if i < 2:
            continue
        if  cline.rstrip().startswith('"'): #filename-->skip the line
            continue

        dstIdx,srcIdx,op,changId = cline.split(',')
        input2orig[int(dstIdx)] = int(srcIdx)
        origline2op[int(srcIdx)] = op
    for pidx, pline in enumerate(prep):
        inputIdx = int(pline.partition(".")[0], 16)
        # ccfx numbers from 1, but pidx is from 0
        pidx2orig[pidx + 1] = input2orig.get(inputIdx, -1)
    meta.prepIdx2OrigIdx = pidx2orig
    meta.line2op = origline2op

print 'map line number finished'
# write all keys in metaDB to a new file
metaDB_key_file = 'metaDB_key_file.txt'
with open(metaDB_key_file, 'w') as f:
    for key in metaDB.name2meta.keys():
        f.write(key+'\n')
print 'write key finished'


ccfx_out_path = 'cross_file.txt'
ccfx_out = RepertoireOutput()
print 'load clone data from file starts...'
ccfx_out.loadFromFile(ccfx_out_path)
print 'load clone data from file ends...'
print 'parsed files: ', len(ccfx_out.files)
print 'parsed clones: ', len(ccfx_out.clones)


files = {}
for fileIdx, path in ccfx_out.getFileIter():
#    print fileIdx
#    print path
    if not metaDB.hasInputPath(path):
        print "Couldn't find meta information for file: ", path
	sys.exit(-1)
    meta = metaDB.getMetaForPath(path)
    files[fileIdx] = meta.filterOutput

clones = {}

for cloneIdx, (clone1, clone2) in ccfx_out.getCloneIter():
    op1 = []
    op2 = []
    fidx1, start1, end1 = clone1
    fidx2, start2, end2 = clone2
    meta1 = metaDB.getMetaForPath(ccfx_out.getFilePath(fidx1))
    meta2 = metaDB.getMetaForPath(ccfx_out.getFilePath(fidx2))

    start1 = meta1.prepIdx2OrigIdx.get(start1+1, -1)
    end1 = meta1.prepIdx2OrigIdx.get(end1, -1)
    start2 = meta2.prepIdx2OrigIdx.get(start2+1, -1)
    end2 = end2 = meta2.prepIdx2OrigIdx.get(end2, -1)

    for i in range(start1,end1+1):
        op = meta1.line2op.get(i, "X")
        op1.append((i,op))

    for i in range(start2,end2+1):
        op = meta2.line2op.get(i, "X")
        op2.append((i,op))

    clone1 = (fidx1, start1, end1, op1)
    clone2 = (fidx2, start2, end2, op2)
    if clone1[0] < clone2[0]:
        clone = (clone1, clone2)
    else:
        clone = (clone2, clone1)
    clones[cloneIdx] = clone

rep_out = RepertoireOutput()
rep_out.loadFromData(files, clones)

# rep_out is the final results, we write out data here
results_file_name = 'inter_group_results.txt'
rep_out.writeToFile(results_file_name)
print "Processing successful!!"
