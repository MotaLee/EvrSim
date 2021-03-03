import pycuda.autoinit
import pycuda.driver as drv
import numpy
from pycuda.compiler import SourceModule

# from core import ESC
src=open('core/escuda/kernel/main.cu')
mod = SourceModule(src.read(),cache_dir='core\\escuda\\bin')
multiply_them = mod.get_function("multiply_them")

a = numpy.random.randn(400).astype(numpy.float32)
b = numpy.random.randn(400).astype(numpy.float32)

dest = numpy.zeros_like(a)
multiply_them(
        drv.Out(dest), drv.In(a), drv.In(b),
        block=(400,1,1), grid=(1,1))

print ( dest-a*b )

def useCuda(kernel=None):
    try:import pycuda.autoinit
    except BaseException:
        ESC.err('Cuda initinizing failed.')

    return
