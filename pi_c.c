#include <math.h>
//#include <omp.h>

double f(double x) {
        return 4./(1. + x*x);
}

double compPi_ctypes(double pi, int niter) {
    double h = 1./niter;
    double x = 0.;
//    omp_set_num_threads(4);
//#pragma omp for
    for (int i=0; i<niter; ++i){
        x = h*(i - 0.5);
        pi += f(x);
    }
    pi *= h;
    return pi;
}