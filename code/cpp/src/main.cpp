#include "iostream"
using namespace std;

#include "exlist.hpp"
#include "es_file.hpp"
#include "dy_struct.hpp"

int main(){
    printf("test start.\n");
    DyStruct ds;

    ds.readJson("t.json");
    // ESFileShell ESS;
    // printf(ESS.esf.header.title);


    printf("test end.\n");
    return 1;
}
