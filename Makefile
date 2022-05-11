CC=gcc
FLAGS=-std=gnu99 -O3 -DNDEBUG -g0 -msse4.2

sum:	sum.c
	$(CC) $(FLAGS) sum.c -o sum

clean:
	rm -f sum
