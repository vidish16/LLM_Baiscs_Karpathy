import math
import matplotlib.pyplot as plt
import numpy as np
class Value:
    def __init__(self,data, _children=(), _op='',label=''):
        self.data=data
        self.grad=0.0
        self._backward= lambda: None
        self._prev= set(_children)
        self._op=_op
        self.label=label
    
    def __repr__(self):
        return f"Value(data={self.data})"
    def __add__(self, other):
        out= Value(self.data + other.data,(self,other),'+')
        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward=_backward
        return out
    def __mul__(self, other):
        out=Value(self.data * other.data,(self,other),'*')
        def _backward():
            self.grad += other.data*out.grad
            other.grad += self.data *out.grad
        out._backward=_backward
        return out

    def tanh(self):
        n=self.data
        t=(math.exp(2*n)-1)/(math.exp(2*n)+1)
        out=Value(t,(self,),'tanh') 
        def _backward():
            self.grad += (1-t**2) * out.grad
        out._backward=_backward
        return out
    def backward(self):
        topo = []
        visited = set()
        
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)

        build_topo(self)
        
        self.grad = 1.0

        for node in reversed(topo):
            node._backward()
