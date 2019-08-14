import numpy as np
import datetime
import os
import dill
import pickle

def generate_exp_name(name=""):
    d=datetime.datetime.today()
    run_name=d.strftime(name+"%Y_%m_%d-%H:%M:%S")
    nb=0
    not_created=True
    while(not_created):
        try:
            os.mkdir(run_name+"_%d"%nb)
            run_name+="_%d"%nb
            not_created=False
        except OSError:
            nb+=1
    return run_name

def dump_pop(pop, gen, run_name="runXXX"):
    out_dict = {"gen": gen, "size": len(pop)}
    for (i,ind) in enumerate(pop):
        out_dict["geno_%d" % i] = np.array(ind)
        if(ind.fitness.valid):
            out_dict["fitness_%d" % i] = ind.fitness.values
            out_dict["novelty_%d" % i] = ind.novelty
            out_dict["bd_%d" % i] = ind.fitness.bd
    try:
        os.mkdir(run_name)
    except OSError:
        pass
    np.savez(run_name+"/pop_gen%d.npz" % gen, **out_dict) 

def dump_archive(archive, gen, run_name="runXXX"):
    out_dict = {"gen": gen, "size": archive.size()}
    for (i,ind) in enumerate(archive.all_bd):
        out_dict["bd_%d" % i] = np.array(ind)
    try:
        os.mkdir(run_name)
    except OSError:
        pass
    np.savez(run_name+"/archive_gen%d.npz" % gen, **out_dict) 

def dump_params(params, run_name="runXXX"):
    try:
        os.mkdir(run_name)
    except OSError:
        pass
    #stat=params["STATS"]
    #params["STATS"]=None # pickle can't save some parts of the stat
    np.savez(run_name+"/params.npz", **params) 
    #params["STATS"]=stat

def dump_logbook(logbook,gen,run_name="runXXX"):
    out_dict = {}
    for k in logbook.header:
        out_dict[k]=logbook.select(k)
    try:
        os.mkdir(run_name)
    except OSError:
        pass
    np.savez(run_name+"/logbook_gen%d.npz" % gen, **out_dict) 
