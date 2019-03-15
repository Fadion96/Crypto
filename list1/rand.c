#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdio.h>


#define MAX 354
#define seed 1

int main () {

	int n = 10;
	int i;
	int r[MAX];
	static char randstate[2048];
    if(initstate(1, randstate, 8)==NULL) {
        printf("Error\n");
    }
	else {
        printf("Success\n");
    }
	// setstate(randstate);
   /* Intializes random number generator */
   /* Print 5 random numbers from 0 to 49 */
   	printf("Random:\n");
   	for(i = 0 ; i < n ; i++ ) {
		printf("%ld\n", random());
	}
	printf("\nImplementation:\n");
	r[0] = seed;
  	for (i=1; i<31; i++) {
    	r[i] = (16807LL * r[i-1]) % 2147483647;
    	if (r[i] < 0) {
      		r[i] += 2147483647;
    	}
  	}
  	for (i=31; i<34; i++) {
    	r[i] = r[i-31];
  	}
  	for (i=34; i<344; i++) {
    	r[i] = r[i-31] + r[i-3];
  	}
  	for (i=344; i<MAX; i++) {
    	r[i] = r[i-31] + r[i-3];
    	printf("%d\n", ((unsigned int)r[i]) >> 1);
  	}
}
