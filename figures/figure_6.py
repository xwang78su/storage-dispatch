import os
from dispatch import Dispatch	# base
a_val = 0
c_val = 1
SoC   = 1 				# q0, preferred SoC
Q0_val  = SoC
test = Dispatch(T=1,a=a_val,c=c_val,Q0=SoC,dQ0=-0.35,QT=None,dQT=None,S=SoC)	# adjust dQ0
test.plot().savefig(f"{os.path.splitext(os.path.basename(__file__))[0]}a_S_1.png",bbox_inches='tight')
test = Dispatch(T=1,a=a_val,c=c_val,Q0=SoC,dQ0=0,QT=None,dQT=1,S=None)			# ok
test.plot().savefig(f"{os.path.splitext(os.path.basename(__file__))[0]}b_dQ.png",bbox_inches='tight')
test = Dispatch(T=1,a=a_val,c=c_val,Q0=SoC,dQ0=0,QT=0.5,dQT=None,S=None)			# note QT -> 0.5
test.plot().savefig(f"{os.path.splitext(os.path.basename(__file__))[0]}c_Q.png",bbox_inches='tight')

