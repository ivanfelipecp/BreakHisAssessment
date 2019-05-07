def begin_accuracy():
    return "\\begin{table}[H] \n\\scalebox{0.6}{ \n\\begin{tabular}{c|c|c|c|c|c|c|c|c|c|} \\cline{2-10} \n& Architecture & A & F & PT & TA & DC & LC & MC & PC \\\\ \\hline"

def end_accuracy(metric):
    return "\end{tabular}} \n\caption{metric} \n\end{table}".replace("metric", metric)

def init_first_row_accuracy(mag):
    return "\multicolumn{1}{|c|}{\multirow{3}{*}" +  "{mag}}".replace("mag",mag)

def init_others_row_accuracy():
    return "\multicolumn{1}{|c|}{}"

def end_others_row_accuracy():
    return "\\\\ \cline{2-10} \n"

def end_final_row_accuracy():
    return "\\\\ \hline \n"

def get_init_row(a, first_arch, mag):
    return init_first_row_accuracy(mag) if (a == first_arch) else init_others_row_accuracy()

def get_end_row(a, last_arch):
    return end_others_row_accuracy() if a != last_arch else end_final_row_accuracy()   

#print(begin_accuracy())
#print(init_first_row_accuracy("40") + example_row + end_others_row_accuracy())
#print(init_others_row_accuracy() + example_row + end_final_row_accuracy())
#print(end_accuracy("pla"))
