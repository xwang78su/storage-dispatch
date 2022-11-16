import numpy as np
from math import cosh, sinh, tanh, sqrt
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from numpy import trapz

class Dispatch:

    # three cases S, dQT, QT
    # start with the case S; run the other two later
    def __init__(self,T,a,c,Q0,dQ0,QT,dQT,S):
        if a<0 or c<0:
            raise Exception("a/c cannot be negative")
        if c == 0:
            w = float('nan')
            if   S != None and dQT == None and QT == None:
                l = - a*T*S
            elif S == None and dQT != None and QT == None:
                # lambda is not feasible in this case
                if dQ0 != 0.0 or dQT != 0.0:
                    raise Exception("constraints on dQ0 and dQT cannot be satisfied")
            elif S == None and dQT == None and QT != None:
                l = - a*T*QT
            else:
                raise Exception("Only one constraint be applied when c=0")            
            pass
        # implement all three cases in this scenario    
        elif a == 0:
            w = float('nan')
            if   S != None and dQT == None and QT == None:
                l = 6*c/T*(S-Q0)-3*c*dQ0
            elif S == None and dQT != None and QT == None:
                l = c*(dQT - dQ0)
            elif S == None and dQT == None and QT != None:
                l = 2*c/T*(QT - dQ0*T - Q0)
            else:
                raise Exception("Only one constraint be applied when a=0")            
            pass
        else:
            w = sqrt(a/c)
            if   S != None and dQT == None and QT == None:
                l = a*w*T**2/sinh(w*T)*(S-dQ0/(w**2*T)*(cosh(w*T)-1)-Q0/(w*T)*sinh(w*T))
            elif S == None and dQT != None and QT == None:
                l = c*T/sinh(w*T)*(dQT-w*Q0*sinh(w*T)-dQ0*cosh(w*T))
            elif S == None and dQT == None and QT != None:
                l = 2*c/T*(QT - dQ0*T - Q0)
            else:
                raise Exception("Only one constraint is needed")
            pass
        self.a = a
        self.T = T
        self.c = c
        self.Q0 = Q0
        self.QT = QT
        self.dQ0 = dQ0
        self.dQT = dQT
        self.S = S
        self.w = w
        self.l = l
    
    def q(self,t):
        if hasattr(t,"__iter__"):
            return [self.q(x) for x in list(t)]
        if self.c == 0:
            return self.S
        elif self.a == 0:
            return self.l/(2*self.c*self.T)*t*t + self.dQ0*t + self.Q0
        else:
            laT = self.l/(self.a*self.T)
            return (self.Q0+laT)*cosh(self.w*t) + (self.dQ0/self.w)*sinh(self.w*t) - laT

    def dq(self,t):
        if hasattr(t,"__iter__"):
            return [self.dq(x) for x in list(t)]
        # check carefully for c = 0
        if self.c == 0:
            if t == 0:
                return float('inf') if self.Q0 > self.S else 0.0 if self.Q0 == self.S else float('-inf')
            elif t == self.T:
                QT = self.q(self.T)
                return float('inf') if self.S > QT else 0.0 if QT == self.S else float('-inf')
            else:
                return 0.0
        elif self.a == 0:
            return self.l/self.c/self.T*t + self.dQ0
        else:
            laT = self.l/(self.a*self.T)
            return self.w*((self.Q0+laT)*sinh(self.w*t) + (self.dQ0/self.w)*cosh(self.w*t))

    def plot(self,t1=1.0,t0=0.0,dt=0.1):
        x = np.arange(t0,t1+dt,dt)

        # calculate the total cost
        fun_q  = 0.5*self.a*np.array(self.q(x))**2
        fun_dq = 0.5*self.c*np.array(self.dq(x))**2
        # use integral
        cost_q = round(trapz(fun_q,  dx=dt), 2)
        cost_dq= round(trapz(fun_dq, dx=dt), 2)
        cost = cost_q + cost_dq
        cost = round(cost, 2)
        print(cost)
        
        # plot out the results
        fig, (ax1,ax2) = plt.subplots(2,1,sharex=True, figsize=(6.4,3.6))
        ax1.plot(x,self.q(x))
        ax1.set_ylabel('Storage ($q$)')
        ax1.grid()
        ax1.legend([f'Total cost: ${cost}'])

        ax2.plot(x,self.dq(x))
        ax2.set_xlabel('Time ($t$)')
        ax2.set_ylabel('Power ($\\dot q$)')
        ax2.grid()


        
        return fig


if __name__ == "__main__":

    import unittest
    TODO = float('nan')
    class TestDispatch(unittest.TestCase):

        def test_ones(self):
            test = Dispatch(T=1,a=1,c=1,Q0=1,dQ0=1,dQT=1,S=1)
            Q = test.q(list(np.arange(0,1,0.1)))
            dQ = test.dq(list(np.arange(0,1,0.1)))
            self.assertEqual(round(test.q(0),4),1.0)
            self.assertEqual(round(test.dq(0),4),1.0)
            self.assertEqual(round(test.q(1),4),1.0)
            self.assertEqual(round(test.dq(1),4),1.0)

        def test_czero(self):
            test = Dispatch(T=1,a=1,c=0,Q0=1,dQ0=1,dQT=1,S=1)
            Q = test.q(list(np.arange(0,1,0.1)))
            dQ = test.dq(list(np.arange(0,1,0.1)))
            self.assertEqual(round(test.q(0),4),1.0)
            self.assertEqual(round(test.dq(0),4),0.0)
            self.assertEqual(round(test.q(1),4),1.0)
            self.assertEqual(round(test.dq(1),4),0.0)

        def test_azero(self):
            test = Dispatch(T=1,a=0,c=1,Q0=1,dQ0=1,dQT=1,S=1)
            Q = test.q(list(np.arange(0,1,0.1)))
            dQ = test.dq(list(np.arange(0,1,0.1)))
            self.assertEqual(round(test.q(0),4),TODO)
            self.assertEqual(round(test.dq(0),4),TODO)
            self.assertEqual(round(test.q(1),4),TODO)
            self.assertEqual(round(test.dq(1),4),TODO)

    unittest.main()

