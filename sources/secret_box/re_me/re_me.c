#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MAX_LEN 128

int check_bank_account(char* name, unsigned int bank_number){
    unsigned int temp_key = 0;
    unsigned int bank_serial[16] = {57730, 47254, 59845, 33181, 19024, 25644, 49250, 32697, 32205, 46996, 11888, 16248, 45767, 50663, 32339, 1825};
    unsigned int masking = 0xdeadbeef;
    for (int i = 0; i < strlen(name); i++){
        // take the last bit of ascii value of each character of name
        temp_key += (name[i] & 1) * bank_serial[i % 16];
    }
    // printf("temp_key: %u\n", temp_key ^ masking);
    if ((temp_key ^ masking) == bank_number){
        return 1;
    }
    return 0;
}

void print_image(FILE *fptr)
{
    char read_string[MAX_LEN];
 
    while(fgets(read_string,sizeof(read_string),fptr) != NULL)
        printf("%s",read_string);
}
int main(){
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    char name[0x20];
    unsigned int bank_number = 0;
    char *filename = "image.txt";
    FILE *fptr = NULL;
 
    if((fptr = fopen(filename,"r")) == NULL)
    {
        fprintf(stderr,"error opening %s\n",filename);
        return 1;
    }
 
    print_image(fptr);
    fclose(fptr);
    
    printf("Send me your name and your bank account number, and then I will send you this 100 dollars!\n");
    printf("Name: ");
    scanf("%32s", name);
    printf("Bank account number: ");
    scanf("%u", &bank_number);
    if (check_bank_account(name, bank_number)){
        printf("Here is your 100 dollars!\n");
        setuid(0);
        system("/bin/bash -i");
    } else {
        printf("You are not the one I am looking for!\n");
    }
    return 0;
}

