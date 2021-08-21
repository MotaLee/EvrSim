#ifndef ES_FILE_H
#define ES_FILE_H
#define DLLEX extern "C" __declspec(dllexport)

typedef struct HeaderBlock{
    char title[11];   // Always 'EVRSIMFILE\n';
    char extension[16];
    char version[16];
};

typedef struct DataBlock{
    DataBlock *addr;
    DataBlock *prev;
    DataBlock *next;
};

// ESFile
typedef struct ESFile{
    HeaderBlock header;
    DataBlock *index;
    DataBlock *first_data;
};

class ESFileShell{
    // private:
    public:
        ESFile esf;
        ESFileShell();
        void initBlock(DataBlock *db);
};

DLLEX ESFile loadESFile(string path);

DLLEX int saveESFile(ESFile *esf);
#endif
