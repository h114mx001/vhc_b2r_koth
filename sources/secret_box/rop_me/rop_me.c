#include <stdio.h> 
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

void win() { 
    setuid(0);
    system("/bin/bash");
}

int main() {
    // printf("Your secret gift: %p", );
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    puts("Welcome to the playground!!!");
    char password[16];  
    puts("Enter the password: ");
    read(0, password, 1000);
    printf("You have typed: ");
    printf("%s", password);
    if (strcmp(password, "password") == 0) {
        printf("You have entered the correct password\n");
    }
    return 0;
}
