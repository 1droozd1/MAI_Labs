CC = gcc
CCFLAGS = -std=c99
SRC = main.c list.c
OBJ = main.o list.o
HD = list.h


start: $(OBJ)
	$(CC) -o main $(OBJ) $(CCFLAGS)
	./main
	rm -f main $(OBJ)

all: $(OBJ)
	$(CC) -o main $(OBJ) $(CCFLAGS)

main.o: $(HD)
	$(CC) $(CCFLAGS) -c main.c

list.o: $(HD)
	$(CC) $(CCFLAGS) -c list.c

clean:
	rm -f main $(OBJ)