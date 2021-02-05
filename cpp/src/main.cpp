#include "iostream"
#include "string.h"
using namespace std;

#include "exlist.h"
#include "es_file.h"

#include <assimp/Importer.hpp>
#include <assimp/scene.h>
#include <assimp/postprocess.h>

int main(){
    printf("test start.\n");

    ESFileShell ESS;
    printf(ESS.esf.header.title);

    Assimp::Importer importer;
    // const aiScene *scene = importer.ReadFile("I:\\OneDrive\\Project\\EvrSim\\1.fbx",
        // aiProcess_Triangulate | aiProcess_FlipUVs);

    printf("test end.\n");
    return 1;
}
