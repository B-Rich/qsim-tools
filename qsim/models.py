import qnet.circuit_components.component as qcp

__all__ = ('Component', 'SLHComponent')

class Component(qcp.Component):
    name = namespace = CDIM = PORTSIN = PORTSOUT = None
    @property
    def name(self):
        return self._name
    @property
    def space(self):
        return self.toSLH().space
    def _substitute(self, var_map): # Fix bug in qcp.Component._substitute
        c = qcp.Component._substitute(self, var_map)
        c.name = self.name
        c.namespace = self.namespace
        return c

class SLHComponent(Component):
    def __init__(self, slh, **parameters):
        parameters['slh'] = slh
        self._parameters = list(parameters.keys())
        #super().__init__('SLH', **parameters)
        super().__init__('SLH_'+','.join(s.label for s in slh.space.local_factors), **parameters)
        self.CDIM = self.slh.L.shape[0]
        # TODO: self.PORTSIN, self.PORTSOUT
    def _toSLH(self):
        return self.slh
