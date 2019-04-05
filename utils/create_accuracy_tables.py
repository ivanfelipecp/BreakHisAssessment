import os
import json
import sys
import numpy as np
from tables_vars_accuracy import *

architectures = ["squeezenet","traditional"]
number_archs = len(architectures)

magnifications = ["40"]

#AUM & CLAHE & DNLM & HE & Original
preprocs = ["um","clahe","dnlm1","he","rgb"]
number_preprocs = len(preprocs)

kfold_dir = "../results/kfold"
results_dir = "/performance/"
epochs = 100
kfold = 5

key_PLA = "patient_level_accuracy"
key_ILA = "image_level_accuracy"


def get_json(filepath):
	with open(filepath, "r") as f:
		datastore = json.load(f)
		return datastore

def search_best(directory):
    best_acc = 0
    best_json = {}
    best_i = 0
    for i in range(epochs):
        file_i = "results_{}.json".format(i)
        results_i = get_json(directory+file_i)
        if results_i[key_ILA] > best_acc:
            best_acc = results_i[key_ILA]
            best_json = results_i
            best_i = i
    print("The best result in {} is {} \n".format(directory, best_i))
    return best_json

def get_best_results(m,a,p):
    current_dir = "{}/{}/{}/{}/".format(kfold_dir, m, a, p)
    dirs = os.listdir(current_dir)
    best_results = {}
    for i in range(kfold):
        print("Looking for best results in {}".format(current_dir))
        best_result = search_best(current_dir+dirs[i]+results_dir)
        best_results[i] = best_result
    return best_results

def get_accuracy(results, key):
    accs = []
    for i in range(kfold):
        accs.append(results[i][key])
    accs = np.array(accs)
    mean = round(np.mean(accs), 2)
    std = round(np.std(accs), 3)
    return [mean, std]

def create_lines(results):
    lines = {key_PLA: {}, key_ILA:{}}
    for i in [key_PLA, key_ILA]:
        for m in magnifications:
            lines[i][m] = {}
            for a in architectures:
                lines[i][m][a] = {}
                current_line = " & {} &".format(a)
                for p in range(number_preprocs):
                    c_p = preprocs[p]
                    [mean, std] = results[m][a][c_p][i]
                    mean = str(mean)
                    std = str(std)
                    std = std[1:]
                    end = " & " if (p+1) < number_preprocs else ""
                    current_line += "${}\\pm{}$".format(mean,std) + end
                lines[i][m][a] = current_line
    return lines                

def main():
    # Get the accuracies of all magnifications
    mags_results = {}
    for m in magnifications:
        arch_results = {}
        # Obtain the mean and std
        for a in architectures:
            arch_results[a] = {}
            for p in preprocs:
                arch_results[a][p] = {}
                # Top 5 best results per fold
                best_results = get_best_results(m,a,p)
                # Mean and STD of PLA
                arch_results[a][p][key_PLA] = get_accuracy(best_results ,key_PLA)
                # Mean and STD of ILA
                arch_results[a][p][key_ILA] = get_accuracy(best_results ,key_ILA)
        # Create the matrix with results
        mags_results[m] = arch_results
    # Create lines in table
    lines = create_lines(mags_results)

    # Create tables
    for j in [key_PLA, key_ILA]:
        table = begin_accuracy()
        for m in magnifications:
            for i in range(number_archs):
                arch_i = architectures[i]
                init_row = get_init_row(i, m)
                line = lines[j][m][arch_i]
                end_row = get_end_row(number_archs, i)
                table += init_row + line + end_row
        metric = "Patient level accuracy mean$\pm$std" if j==key_PLA else "Image level accuracy mean$\pm$std"
        table += end_accuracy(metric)
        print(table + "\n")
main()
