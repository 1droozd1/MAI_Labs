CC = gcc
CCFLAGS = -std=c99
SRC = main.c sort.c
OBJ = main.o sort.o
HD = sort.h

all: $(OBJ)
	$(CC) -o main $(OBJ) $(CCFLAGS)

start: $(OBJ)
	$(CC) -o main $(OBJ) $(CCFLAGS)
	./main
	rm -f main $(OBJ)
	ma
main.o: $(HD)
	$(CC) $(CCFLAGS) -c main.c

sort.o: $(HD)
	$(CC) $(CCFLAGS) -c sort.c

pre:
	$(CC) -c $(SRC)

clean:
	rm -f main $(OBJ)