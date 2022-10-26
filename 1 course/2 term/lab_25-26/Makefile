CC = gcc
CCFLAGS = -std=c99
SRC = main.c deck.c
OBJ = main.o deck.o
HD = deck.h

all: $(OBJ)
	$(CC) -o main $(OBJ) $(CCFLAGS)
	./main
	rm -f main $(OBJ)

main.o: $(HD)
	$(CC) $(CCFLAGS) -c main.c

deck.o: $(HD)
	$(CC) $(CCFLAGS) -c deck.c

pre:
	$(CC) -c $(SRC)

clean:
	rm -f main $(OBJ)