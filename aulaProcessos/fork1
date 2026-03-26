#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int a=2;
int main() {
	   pid_t pid;
	   if ((pid = fork()) == 0) {
		a = a + 2;
	        printf("\nValor de a no filho=%d", a);
	   }
	   else {
		sleep(2);
		a = a + 5;
	        printf("\nValor de a no pai=%d", a);
	   }
return 0;
}
