#! /usr/bin/env python3
import argparse
import os
import subprocess

def create_readoutcfg(cfgname, inputfilename, timeout = 60):
    with open(cfgname) as writer:
        writer.write("[readout]\n")
        writer.write("rate=-1\n")
        writer.write("exitTimeout=%d\n" %timeout)
        writer.write("disableAggregatorSlicing = 1\n")
        writer.write("[bank-default]\n")
        writer.write("type=malloc\n")
        writer.write("size=2G\n")
        writer.write("[equipment-player-1]\n")
        writer.write("name=player-1\n")
        writer.write("enabled=1\n")
        writer.write("filePath=/clusterfs2/markus/o2/Run3Conversion/rawtest/emcal.raw\n" %inputfilename)
        writer.write("memoryPoolNumberOfPages=1000\n")
        writer.write("memoryPoolPageSize=2M\n")
        writer.write("preLoad=0\n")
        writer.write("autoChunk=1\n")
        writer.write("[consumer-stats]\n")
        writer.write("consumerType=stats\n")
        writer.write("enabled=1\n")
        writer.write("monitoringEnabled=1\n")
        writer.write("monitoringUpdatePeriod=5\n")
        writer.write("monitoringURI=infologger://\n")
        writer.write("[consumer-data-sampling]\n")
        writer.write("consumerType=DataSampling\n")
        writer.write("enabled=1\n")
        writer.close()

def find_files(inputdir, filebase):
    allfiles = []
    for root,dirs,files in os.walk(inputdir):
        for f in files:
            if filebase in f:
                allfiles.append(os.path.join(root, f))
    return allfiles

def main(inputdir, filebase, nfiles, timeout = 60):
    allfiles = find_files(inputdir, filebase)
    nprocessed = 0 
    for f in allfiles:
        cfgname = "/tmp/readout_replay_%d.cfg" %nprocessed
        if os.path.exists(cfgname):
            os.remove(cfgname)
        create_readoutcfg(cfgname, f)
        subprocess.call("readout.exe file://%s" %cfgname, shell=True)
        nprocessed += 1
        if nfiles > 0 and nprocessed == nfiles:
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser("runReadout.py", "Run readout.exe for a chain of raw files")
    parser.add_argument("-i", "--inputdir", required =True, type = str, help = "Location where to search for input files")
    parser.add_argument("-f", "--filename", type = str, default = "emcal.raw", help = "Name of the raw file")
    parser.add_argument("-n", "--nfiles", type = int, default = -1, help = "Max. number of files")
    parser.add_argument("-t", "--timeout", type = int, default = 60, help = "Timeout (in seconds)")
    args = parser.parse_args()
    main(args.inputdir, args.filename, args.nfiles, args.timeout)