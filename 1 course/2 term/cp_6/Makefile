CC = gcc
CCFLAGS = -std=c99
SRC = main.c project.c
OBJ = main.o project.o
HD = project.h

start: $(OBJ)
	$(CC) -o main $(OBJ) $(CCFLAGS)
	./main
	rm -f main $(OBJ)

all: $(OBJ)
	$(CC) -o main $(OBJ) $(CCFLAGS)

create: print_in_file.o project.o 
	$(CC) -o print_in_file print_in_file.o project.o 
	./print_in_file
	rm -f print_in_file print_in_file.o project.o  

print_in_file.o: $(HD)
	$(CC) $(CCFLAGS) -c print_in_file.c

main.o: $(HD)
	$(CC) $(CCFLAGS) -c main.c

project.o: $(HD)
	$(CC) $(CCFLAGS) -c project.c

clean:
	rm -f main print_in_file $(OBJ) print_in_file.o