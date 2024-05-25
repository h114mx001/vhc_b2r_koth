#include <stdio.h> 
#include <stdlib.h>

int main() {
    char password[16];  
    printf("Enter the password: ");
    read(0, password, 1000);
    puts("You entered: ");
    puts(password);
    return 0;
}
