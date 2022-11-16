import os
from dispatch import Dispatch
test = Dispatch(T=1,a=1,c=0,Q0=1,dQ0=0,QT=None,dQT=None,S=1)
test.plot().savefig(f"{os.path.splitext(os.path.basename(__file__))[0]}a_S.png",bbox_inches='tight')
