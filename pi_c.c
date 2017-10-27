#include <math.h>
#include <omp.h>

double f(double x) {
        return 4./(1. + x*x);
}

double compPi_ctypes(double pi, int niter) {
    double h = 1./niter;
    double x = 0.;
#pragma omp parallel for reduction(+:pi) private(x)
    for (int i=0; i<niter; ++i){
        x = h*(i - 0.5);
        pi += f(x);
    }
    pi *= h;
    return pi;
}
