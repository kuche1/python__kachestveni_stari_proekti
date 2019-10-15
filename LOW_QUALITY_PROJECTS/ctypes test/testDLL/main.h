#ifndef __MAIN_H__
#define __MAIN_H__

#include <windows.h>

/*  To use this exported function of dll, include this header
 *  in your project.
 */

#ifdef BUILD_DLL
    #define DLL_EXPORT __declspec(dllexport)
#else
    #define DLL_EXPORT __declspec(dllimport)
#endif


#ifdef __cplusplus
extern "C"
{
#endif

void DLL_EXPORT SomeFunction(const LPCSTR sometext);
int DLL_EXPORT add1(int num1){
    return num1+1;
}
int DLL_EXPORT add(int num1,int num2){
    return num1+num2;
}

#ifdef __cplusplus
}
#endif

#endif // __MAIN_H__
