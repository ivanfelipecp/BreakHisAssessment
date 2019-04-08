import os
import json
import sys
import numpy as np
from tables_vars_multi import *

architectures = ["squeezenet","traditional"]
number_archs = len(architectures)

magnifications = ["40", "117"]

#AUM & CLAHE & DNLM & HE & Original
preprocs = ["um","clahe","dnlm1","he","rgb"]
number_preprocs = len(preprocs)

kfold_dir = "../results/kfold"
results_dir = "/performance/"
epochs = 100
kfold = 5
classes = 8

key_ACC = "ACC"
key_PPV = "PPV"
key_TPR = "TPR"
key_ILA = "image_level_accuracy"

key_F1 = (key_PPV, key_TPR)

keys = [key_ACC, key_F1]

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

def roundi(array, r):
  array = array.tolist()
  f = lambda x: round(x, r)
  return list(map(f, array))    

def get_mean_std(array):
	array = np.array(array)
	mean = np.mean(array, axis=0)
	std = np.std(array, axis=0)
	return (mean,std)

def F1(ppv, tpr):
	return 2*((ppv*tpr)/(ppv+tpr))

def get_F1(results):
	ppv = []
	tpr = []
	for i in range(kfold):
		ppv.append(results[i][key_PPV])
		tpr.append(results[i][key_TPR])

	ppv = np.array(ppv)
	
	(ppv_mean, ppv_std) = get_mean_std(ppv)
	(tpr_mean, tpr_std) = get_mean_std(tpr)

	F1_mean = roundi(F1(ppv_mean, tpr_mean), 2)
	F1_std = roundi(F1(ppv_std, tpr_std), 2)

	return [F1_mean, F1_std]

def get_accuracy(results):
	accs = []
	for i in range(kfold):
		accs.append(results[i][key_ACC])
	(mean,std) = get_mean_std(accs)
	mean = roundi(mean, 2)
	std = roundi(std, 3)
	return [mean, std]

def mean_std_to_str(mean, std):
	ret = ""
	for i in range(classes):
		m = str(mean[i])
		s = str(std[i])
		s = s[1:]
		end = " & " if i+1 != classes else " "
		ret += "${}\\pm{}$".format(m,s) + end
	return ret        


def create_lines(results):
	lines = {key_ACC: {}, key_F1:{}}  
	for i in keys:
		for m in magnifications:
			lines[i][m] = {}
			for a in architectures:
				lines[i][m][a] = {}
				for p in preprocs:
					[mean, std] = results[m][a][p][i]
					current_line = " & {} &".format(a) + mean_std_to_str(mean, std)
					lines[i][m][a][p] = current_line
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
				arch_results[a][p][key_ACC] = get_accuracy(best_results)
				# Mean and STD of ILA
				arch_results[a][p][key_F1] = get_F1(best_results)
		# Create the matrix with results
		mags_results[m] = arch_results
	# Create lines in table
	lines = create_lines(mags_results)
	# Create tables

	for j in keys:
		for p in preprocs:
			table = begin_accuracy()
			for m in magnifications:
				for a in architectures:
					init_row = get_init_row(a, architectures[0], m)
					line = lines[j][m][a][p]
					end_row = get_end_row(a, architectures[0])
					table += init_row + line + end_row
			metric = "{} accuracy per class mean$\pm$std".format(p) if j==key_ACC else "{} F1-score per class mean$\pm$std".format(p)
			table += end_accuracy(metric)
			print(table + "\n")
			input()
	"""
	for j in keys:
		table = begin_accuracy()
		for m in magnifications:
			for i in range(number_archs):
				arch_i = architectures[i]
				init_row = get_init_row(i, m)
				line = lines[j][m][arch_i]
				end_row = get_end_row(number_archs, i)
				table += init_row + line + end_row
		metric = "Accuracy per class mean$\pm$std" if j==key_ACC else "F1-score per class mean$\pm$std"
		table += end_accuracy(metric)
		print(table + "\n")
	"""        
main()