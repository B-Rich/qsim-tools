import qnet.algebra.hilbert_space_algebra as qna
import qnet.circuit_components.component as qcp

import sympy as sp

__all__ = ('Component', 'SLHComponent')

class Component(qcp.Component):
    name = namespace = CDIM = PORTSIN = PORTSOUT = None

    def _space(self):
        return self.toSLH().space
    def _substitute(self, var_map): # Fix bug in Component._substitute
        c = qcp.Component._substitute(self, var_map)
        c.name = self.name
        c.namespace = self.namespace
        return c

class SLHComponent(Component):
    name = 'SLH'

    def __init__(self, slh, **parameters):
        parameters['slh'] = slh
        self._parameters = list(parameters.keys())
        super().__init__(SLHComponent.name, slh.space.__str__(), **parameters)
        self.CDIM = self.slh.L.shape[0]
        # TODO: self.PORTSIN, self.PORTSOUT

    def _toSLH(self):
        return self.slh
