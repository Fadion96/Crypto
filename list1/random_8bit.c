#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main () {
	static char randstate[2048];
	if (argc == 3) {
			initstate(atoi(argv[2]), randstate, 8);
	} else {
			initstate(1, randstate, 8);
	}

	if (argc >= 2) {

			int limit = atoi(argv[1]);
			for (int i = 0; i < limit; i++) {
					printf("%ld\n", random());
			}
	}

	return 0;
}
