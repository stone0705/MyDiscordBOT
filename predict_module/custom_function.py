import gplearn.functions as gp_func
import numpy as np

def _logical(x1, x2, x3, x4):
    return np.where(x1 > x2, x3, x4)


def get_custom_function_list():
    function_list = ['add', 'sub', 'mul', 'div']
    function_list.append(gp_func.make_function(function=_logical,name='logical',arity=4))
    return function_list