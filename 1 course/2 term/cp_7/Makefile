CC = gcc
CCFLAGS = -std=c99
SRC = main.c vector.c
OBJ = main.o vector.o
HD = vector.h

all: $(OBJ)
	$(CC) -o main $(OBJ) $(CCFLAGS)

main.o: $(HD)
	$(CC) $(CCFLAGS) -c main.c

vector.o: $(HD)
	$(CC) $(CCFLAGS) -c vector.c

pre:
	$(CC) -c $(SRC)

clean:
	rm -f main $(OBJ)