#ifndef DY_STRUCT_HPP
#define DY_STRUCT_HPP
using namespace std;

typedef int TYPE;
typedef int POS;
typedef string FIELD;

#include "nlohmann/json.hpp"
using json = nlohmann::json;

struct DyStruct {
    public:
    char* ptr_dict;
    std::map<FIELD, std::pair<TYPE, POS>> dict;
    json _json_obj;

    void initDict(const string path);
    void readJson(const string& path);
};
#endif
