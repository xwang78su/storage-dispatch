"""Update table_3.tex based on input from table_2.csv"""

import csv
from dispatch import Dispatch   # base

varlist = {}

with open('table_2.csv','rt') as fh:
    reader = csv.reader(fh)
    for cell in reader:
        globals()[cell[0]] = varlist[cell[0]] = float(cell[2].strip('$%').replace(',',''))

# TODO implement calculations here based imported globals()
for name,value in varlist.items():
    print(name,'=',value)

Cbase = Dispatch(T=1,a=a_base,c=c,Q0=1-Q,dQ0=-0.05,QT=None,dQT=None,S=1-Q).cost()
Ccase = Dispatch(T=1,a=a_case,c=c,Q0=1-Q,dQ0=-0.05,QT=None,dQT=None,S=1-Q).cost()

with open('table_3.tex','wt') as tex:
    print("\\begin{tabular}{|l|c|c|c|}",file=tex)
    print("\\hline",file=tex)
    print(" & Base Case & Study Case & Savings \\\\ \\hline",file=tex)
    print(' & '.join(["Net cost / savings",f"$${Cbase:.2f}/h",f"$${Ccase:.2f}/h",f"{(1-Ccase/Cbase)*100:.1f}%%"]).replace('$$','\\$').replace('%%','\\%'),file=tex)
    print("\\\\ \\hline",file=tex)
    print("\\end{tabular}",file=tex)

