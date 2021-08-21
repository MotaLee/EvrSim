#include "string.h"
#include "exlist.hpp"
ExList::ExList(int s=0){
    if(s==0) ptr=nullptr;
    else ptr=new int[s];
}

// 2. 复制构造函数
ExList::ExList(const ExList &a){
    if(a.ptr==nullptr){
        ptr=nullptr;
        size=0;
    }else{
        ptr=new int[a.size];
        memcpy(ptr, a.ptr, sizeof(int)*a.size); // 拷贝原数组内容
        size=a.size;
    }
}

// 3. 拷贝构造函数
ExList::~ExList(){
    if(ptr) delete [] ptr;
}

// 4. 重载赋值=运算符函数
ExList & ExList::operator=(const ExList & a){
    if(ptr==a.ptr)return *this;
    if(a.ptr==nullptr){
        if(ptr) delete [] ptr;
        ptr=nullptr;
        size=0;
        return *this;
    }
    if(size < a.size){
        if(ptr) delete [] ptr;
        ptr=new int[a.size];
    }
    memcpy(ptr, a.ptr, sizeof(int)*a.size); // 拷贝原数组内容
    size=a.size;
    return *this;
}

// 5. 重载[]运算符函数
int & ExList::operator[](int i){
    return ptr[i];
}

// 6. 在数组的末尾加入一个新的元素
void ExList::append(int v){
    if(ptr){
    // 如果数组不为空
        int *tmpPtr=new int[size + 1]; // 重新分配空间
        memcpy(tmpPtr, ptr, sizeof(int)*size); // 拷贝原数组内容
        delete [] ptr;
        ptr=tmpPtr;
    }else{
        // 如果数组本来就是空的
        ptr=new int[1];
    }
    ptr[size++]=v; //加入新的数组元素
}

// 7. 获取数组的长度
int ExList::length(){
    return size;
}
