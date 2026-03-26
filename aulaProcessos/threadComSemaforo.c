#include <pthread.h>
#include <semaphore.h>
#include <stdio.h>
#include <stdlib.h>

pthread_t trd_1, trd_2;
sem_t s0, s1;

float shared = 0;

void *thread_0() {
	long int i;
	for(i=0; i<1000000; i++) {
		sem_wait(&s0);
		shared = shared + 1;
		sem_post(&s0);
	}
}


void *thread_1() {
	long int i;
	for (i=0; i<2000000; i++) {
		sem_wait(&s0);
		shared = shared + 1;
		sem_post(&s0);
	}
}

int main() {
	int result;
	sem_init(&s0, 0, 1);
	sem_init(&s1, 0, 0);
	result = pthread_create(&trd_1, NULL, thread_0, NULL);
	result = pthread_create(&trd_2, NULL, thread_1, NULL);
	pthread_join(trd_1, (void **) &result);
	pthread_join(trd_2, (void **) &result);
	printf("Shared = %f\n", shared);
	return(0);
}



