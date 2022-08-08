/* Written by Nicholas Duncan N01451197
 * COP4610 Operating systems
 */
//import necessary libraries
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include<unistd.h>
//main
int main(int argc, char* argv[]){
	printf("Welcome to Nic's DOS interpreter\n");
	//loop until the user enters Ctr+C to exit
	int exit = 0;
	while(exit == 0){
		printf("Press Crtl+C to exit\n");
		//initialize a character pointer for input
		char* input = malloc(512 * sizeof(char));
		memset(input, '\0', 512 * sizeof(char));
		//get user command input
		printf(">");
		//will read until the end of the line
		fgets(input, 512, stdin);
		fclose;
		//printf("%s\n", input);
		
		//break up input into command, arg1, and arg2
		char* command = malloc(512 * sizeof(char));
		memset(command, '\0', 512 * sizeof(char));
		char* arg1 = malloc(512 * sizeof(char));
		memset(arg1, '\0', 512 * sizeof(char));
		char* arg2 = malloc(512 * sizeof(char));
		memset(arg2, '\0', 512 * sizeof(char));
		char* combine = malloc(512 * sizeof(char));
		memset(combine, '\0', 512 * sizeof(char));
		//copy results of input to variables
		command = strtok(input, " \r\t\n");
		arg1 = strtok(NULL, " \r\t\n");
		arg2 = strtok(NULL, " \r\t\n");
		//TESTING: print out command
		//printf("Command: %s, arg1: %s, arg2: %s\n", command, arg1, arg2);
			
		//completed, needs validation	
		//Dos: cd, Unix: cd
		if(strcmp(command, "cd") == 0){
			printf("cd detected\n");
			//cd must have a valid arg 1 only
			if(arg1 == NULL || arg2 != NULL){
				printf("WARNING: command can only accept one valid arguement\n");
				continue;
			}//end if
			//strcpy(combine, "cd");
			//strcat(combine, " ");
			//strcat(combine, arg1);
			//printf("Resulting command: %s\n", combine);
			//system(combine);
			//In order to change the active directory, use chdir
			chdir(arg1);
			//Print out the current working directory
			system("pwd");
		}//end if

		//complete
		//Dos: dir, Unix: ls
		else if(strcmp(command, "dir") == 0){
			//printf("dir detected\n");
			//If there is no arg2, simply perform ls on the current directory.
			if(arg1 == NULL){
				system("ls");
			}//end if
			//If arg1 does contain a subfolder destination, perform ls on that folder
			else{
				//run the ls command with the destination from arg1 inside
				//TODO figure out how to make it see folders properly
				strcpy(combine, "ls");
				strcat(combine, " ");
				strcat(combine, arg1);
				//printf("Resulting command: %s\n", combine);
				system(combine);
			}//end else
		}//end else if
		
		//completed
		//Dos: type, Unix: cat
		//displays contents of a selected file
		else if(strcmp(command, "type") == 0){
			printf("type detected\n");
			//must have a valid arg1 and no arg2
			if(arg1 == NULL || arg2 != NULL){
				printf("WARNING: command can only accept only one valid arguement\n");
				continue;
			}//end if
			
			//build the full command to send to the system
			strcpy(combine, "cat");
			strcat(combine, " ");
			strcat(combine, arg1);
			//printf("Resulting command: %s\n", combine);
			system(combine);
		}//end else if
		
		//completed	
		//Dos: del, Unix: rm
		else if(strcmp(command, "del") == 0){
			printf("del detected\n");
			//must have a valid arg1 and no arg2
			if(arg1 == NULL || arg2 != NULL){
				printf("WARNING: command can accept only one valid arguement\n");
				continue;
			}//end if

			
			strcpy(combine, "rm");
			strcat(combine, " ");
			strcat(combine, "-r");
			strcat(combine, " ");
			strcat(combine, arg1);
			//printf("Resulting command: %s\n", combine);
			system(combine);
		}//end else if
		
		//completed
		//Dos: ren, Unix: mv
		//used to rename a file or directory in this circumstance
		else if(strcmp(command, "ren") == 0){
			printf("ren detected\n");
			//must have a valid arg1(target) and arg2(new name)
			if(arg1 == NULL || arg2 == NULL){
				printf("WARNING: command requires two arguements\n");
				continue;
			}//end if


			//assemble the command
			strcpy(combine, "mv");
			strcat(combine, " ");
			strcat(combine, arg1);
			strcat(combine, " ");
			strcat(combine, arg2);
			//printf("Resulting command: %s\n", combine);
			system(combine);
		}//end else if
		
		//completed	
		//Dos: copy, Unix: cp
		//Makes a simple copy of a file or folder
		else if(strcmp(command, "copy") == 0){
			printf("copy detected\n");
			//must have a valid arg1 and arg2 passed
			if(arg1 == NULL || arg2 == NULL){
				printf("WARNING: command requires two arguements\n");
				continue;
			}//end if

			//Build the command
			strcpy(combine, "cp");
			strcat(combine, " ");
			strcat(combine, "-r");
			strcat(combine, " ");
			strcat(combine, arg1);
			strcat(combine, " ");
			strcat(combine, arg2);
			//printf("Resulting command: %s\n", combine);
			system(combine);
		}//end else if
		
		
		//unrecognized command
		else{
			printf("Unrecognized command\n");
			continue;
			
		}//end else
	}//end while

}//end main
