#include <stdlib.h>
#include <stdio.h>

int main(int argc, char *argv[]) {

    if (argc == 3) {
        srandom(atoi(argv[2]));
    } else {
        srandom(4234234);
    }

    if (argc >= 2) {
        int limit = atoi(argv[1]);
        for (int i = 0; i < limit; i++) {
            printf("%ld\n", random());
        }
    }

    return 0;
}
