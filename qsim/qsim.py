from math import ceil

import qutip as qt
import numpy as np
import functools as ft

from qnet.algebra.hilbert_space_algebra import ProductSpace, BasisRegistry

__all__ = ('trunc_check', 'basis_expand', 'QSimModel')

def trunc_check(state):
    data = []
    for ind in range(len(state.dims[0])):
        rho = state.ptrace(ind)
        data.append([np.real(rho[i,i]) for i in range(rho.shape[0])])
    return data

def basis_expand(fun, **kwargs):
    return ft.partial(fun,**kwargs)

def basis_adjust(trunc_check):
    new_dims = []
    for p in trunc_check:
        tail = sum(p[-ceil(len(p)/5):])
        new_dims.append(ceil(len(p)*(1+tail)) if tail>1e-2 else len(p))
    return new_dims

class QSimModel(object):
    def __init__(self, slh_model):
        self.slh = slh_model
        self.dims = [10]*len(self.space)
        self.dtime = 1e-3

    @property
    def space(self):
    	return self.slh.space.local_factors() # use @property local_factors when available

    @property
    def dims(self):
        return [s.dimension for s in self.space]
    @dims.setter
    def dims(self, dims):
        for s,N in zip(self.space,dims):
            s.dimension = N

    def mesolve(self, time, states0=basis_expand(qt.basis,n=0), e_ops=[],
        dim_max=1000, verbose=True):
        t = np.arange(0, time, self.dtime)
        if not isinstance(states0,list):
            states0 = [states0]*len(self.space)
        while np.product(self.dims) <= dim_max:
            H, L = self.slh.HL_to_qutip()
            state0 = qt.tensor([s(n) for (s,n) in zip(states0,self.dims)])
            sol = qt.mesolve(H, state0, t, L, e_ops, progress_bar=verbose)
            new_dims = basis_adjust(trunc_check(sol.states[-1]))
            if self.dims != new_dims:
                self.dims = new_dims
                if verbose: print("Updating basis size: " + str(self.dims))
            else: return sol
        if verbose:
            print("Max dimensionality exceeded.")
        return sol
