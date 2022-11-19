"""Update table_3.tex based on input from table_2.csv"""

import csv
from dispatch import Dispatch   # base

varlist = {}

with open('table_2.csv','rt') as fh:
    reader = csv.reader(fh)
    for cell in reader:
        globals()[cell[0]] = varlist[cell[0]] = float(cell[2].strip('$%').replace(',',''))

print("INPUTS")
for name,value in varlist.items():
    print(f"{name:10s} = {value}")

ask = 0.1
Q0 = 1-Q
dQ0 = P/2
QT = 1-Q + ask
dQT = None
S = None

print("PARAMETERS")
for name in ["Q0","dQ0","QT","dQT","S"]:
    value = globals()[name]
    print(f"{name:10s} = {value}")

Cbase = Cmon/768 + ask*Pp
Ccase = Dispatch(T=1,a=a_case,c=c,Q0=Q0,dQ0=0,QT=QT,dQT=dQT,S=S).cost()

with open('table_3.tex','wt') as tex:
    print("\\begin{tabular}{|l|c|c|c|}",file=tex)
    print("\\hline",file=tex)
    print(" & Base Case & Study Case & Savings \\\\ \\hline",file=tex)
    print(' & '.join(["Net cost / savings",f"$${Cbase:.2f}/h",f"$${Ccase:.2f}/h",
        f"{(1-Ccase/Cbase)*100:.1f}%%"]).replace('$$','\\$').replace('%%','\\%'),file=tex)
    print("\\\\ \\hline",file=tex)
    print("\\end{tabular}",file=tex)

Dispatch(T=1,a=a_case,c=c,Q0=Q0,dQ0=0,QT=QT,dQT=dQT,S=S).plot().savefig("case.png")