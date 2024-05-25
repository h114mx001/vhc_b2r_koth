#include <unistd.h>
#include <stdlib.h>
// thanks so much stackoverflow to help me to run a python script as root :)
// https://stackoverflow.com/questions/8314012/setuid-bit-on-python-script-linux-vs-solaris 
int main(int argc, char **argv){
    setuid(0);
    system("/home/werkzeug/sources/secret_box/crypto_me/crypto_me.py");
    return 0;
}