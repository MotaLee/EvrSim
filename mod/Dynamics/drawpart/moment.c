struct Header{
    char header[12];
    bool binary;
    char file_type[16];
    char version[16];
}HEADER={
    'EVRSIM_FILE',
    false,
    'Drawpart',
    '0.0.12'
};

struct EStructIndex{
    int len_index;

};


STRUCT_INDEX={int:,float:,char:8,bool:1,,'Pt':20,'Element':0,'Mesh':0}
Pt={
    position:float[3]
    tex_cs:float[2]
}
Element={

}

SC000100000000000000000000
