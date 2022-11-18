"""Update table_2.tex based on input from table_2.csv"""
import csv
with open('table_2.tex','wt') as tex:
    print("\\begin{tabular}{|l|rl|}",file=tex)
    print("\\hline",file=tex)
    with open('table_2.csv','rt') as fh:
        reader = csv.reader(fh)
        for cell in reader:
            print(' & '.join(cell[1:]).replace('$$','\\$').replace('%%','\\%'),end='\\\\ \\hline\n',file=tex)
    print("\\end{tabular}",file=tex)