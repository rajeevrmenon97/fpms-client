TARGET=scanner

CC=gcc
CFLAGS=-Wall -O2 -I./

LIBUSB_DLIB=-lm -lstdc++
FTRSCANAPI_DLIB=./libScanAPI.so

all: $(TARGET)

$(TARGET): $(TARGET).c
	$(CC) $(CFLAGS) -o $(TARGET) $(TARGET).c $(FTRSCANAPI_DLIB) $(LIBUSB_DLIB)

clean:
	rm -f $(TARGET)
