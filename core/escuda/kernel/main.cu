#include <cmath>
// #include <map>
#include <vector>
// #include <sstream>
// #include <stdexcept>
// #include <cstdlib>

__global__ void multiply_them(float *dest, float *a, float *b){
    const int i = threadIdx.x;
    dest[i] = a[i] * b[i];
}
