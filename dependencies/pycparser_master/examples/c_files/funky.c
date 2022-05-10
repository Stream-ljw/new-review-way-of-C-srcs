char foo(void)
{
    return '1';
}

char foo1(void)
{
    return '1';
}

char foo2(void)
{
    return '1';
}

char foo3(void)
{
    char o = foo();
    return '1';
}

int maxout_in(int paste, int matrix)
{
    char o = foo3();
    char p = foo2();
    return  matrix * 5 - paste;
}

int main()
{
    auto char* multi = "a multi";
    
    int paste = 1 ;
    int matrix = 2;
    res = maxout_in(paste, matrix);
    return 0;
}



