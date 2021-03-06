def begin_accuracy():
    return "\\begin{table}[H] \n\\scalebox{0.6}{ \n\\begin{tabular}{c|c|c|c|} \cline{2-4} \n& \diagbox[]{Architecture}{Preprocessing} & AUM & Original \\\\ \\hline"

def end_accuracy(metric):
    return "\end{tabular}} \n\caption{metric} \n\end{table}".replace("metric", metric)

def init_first_row_accuracy(mag):
    return "\multicolumn{1}{|c|}{\multirow{3}{*}" +  "{mag}}".replace("mag",mag)

def init_others_row_accuracy():
    return "\multicolumn{1}{|c|}{}"

def end_others_row_accuracy():
    return "\\\\ \cline{2-4} \n"

def end_final_row_accuracy():
    return "\\\\ \hline \n"

def get_init_row(i, mag):
    return init_first_row_accuracy(mag) if (i == 0) else init_others_row_accuracy()

def get_end_row(number, i):
    return end_others_row_accuracy() if (i+1) < number else end_final_row_accuracy()   

#print(begin_accuracy())
#print(init_first_row_accuracy("40") + example_row + end_others_row_accuracy())
#print(init_others_row_accuracy() + example_row + end_final_row_accuracy())
#print(end_accuracy("pla"))
