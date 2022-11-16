import os
from dispatch import Dispatch	# study
a_val = 0.32
c_val = 2
SoC   = 1 				# q0, preferred SoC
Q0_val  = SoC
# dQ0_val = -0.05		# need to choose carefully for each scenario
test = Dispatch(T=1,a=a_val,c=c_val,Q0=SoC,dQ0=-0.05,QT=None,dQT=None,S=SoC)
test.plot().savefig(f"{os.path.splitext(os.path.basename(__file__))[0]}.png",bbox_inches='tight')
