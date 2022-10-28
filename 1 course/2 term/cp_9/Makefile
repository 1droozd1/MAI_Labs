CC = gcc
CCFLAGS = -std=c99
SRC = main.c massive.c
OBJ = main.o massive.o
HD = massive.h


start: $(OBJ)
	$(CC) -o main $(OBJ) $(CCFLAGS)
	./main
	rm -f main $(OBJ)

all: $(OBJ)
	$(CC) -o main $(OBJ) $(CCFLAGS)

main.o: $(HD)
	$(CC) $(CCFLAGS) -c main.c

massive.o: $(HD)
	$(CC) $(CCFLAGS) -c massive.c

clean:
	rm -f main $(OBJ)