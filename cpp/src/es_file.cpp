#include "iostream"
#include "fstream"
#include "cstring"
using namespace std;

#define DLLEX extern "C" __declspec(dllexport)
#include "exlist.h"
#include "es_file.h"
//两数相加

ESFileShell::ESFileShell(){
    strcpy(esf.header.title,"EVRSIMFILE\n");
}

DLLEX ESFile loadESFile(string path){
    ESFile esf;
    ifstream infile;   //输入流
    // ofstream outfile;   //输出流
    infile.open(path, ios::in);
    return esf;
}

DLLEX int saveESFile(ESFile *esf){
    return 1;
}
