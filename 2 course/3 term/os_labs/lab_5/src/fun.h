#ifndef __LIB_H__
#define __LIB_H_

#include "stdlib.h"
#include "stdio.h"


#if OS == APPLE
typedef short os_int;
typedef long double os_float;

#elif OS == UNIX
typedef long os_int;
typedef double os_float;

#elif OS == WIN32
typedef int os_int;
typedef float os_float;
#endif


extern os_int *GCD(os_int A, os_int B);
extern os_int *Sort(os_int *array);

#endif