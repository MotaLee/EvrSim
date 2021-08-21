#include <fstream>
#include "dy_struct.hpp"
using namespace std;
// using std::string;
void DyStruct::initDict(const string path) {

}

/* Read json via giving path.
    * Para path:;
*/
void DyStruct::readJson(const string & path) {
    std::ifstream(path) >> _json_obj;
}
