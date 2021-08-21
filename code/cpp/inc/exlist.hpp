#ifndef EXLIST_H
#define EXLIST_H

class ExList{
    public:
        int size; // 数组元素的个数
        int* ptr;  // 指向动态分配的数组
        ExList(int s);
        ExList(const ExList &a);
        ~ExList();
        ExList & operator=(const ExList & a);
        int & operator[](int i);
        void append(int v);
        int length();
};

#endif
