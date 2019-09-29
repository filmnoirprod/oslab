###################################################
#
# Makefile
# Simple example for cryptodev-linux
#
# Stefanos Gerangelos <sgerag@cslab.ece.ntua.gr>
# Vangelis Koukis <vkoukis@cslab.ece.ntua.gr>
#
###################################################

CC = gcc

CRYPTODEVDIR=$(HOME)/ask3/virtio-crypto-helpcode-20180430/cryptodev/cryptodev-linux-1.9

CFLAGS = -Wall -I$(CRYPTODEVDIR)
CFLAGS += -g
# CFLAGS += -O2 -fomit-frame-pointer -finline-functions

LIBS = 

BINS = crypto-test server client

all: $(BINS)

crypto-test: crypto-test.c
	$(CC) $(CFLAGS) -o $@ $< $(LIBS)

server: server.c socket-common.h
	$(CC) $(CFLAGS) -o $@ $< $(LIBS)

client: client.c socket-common.h
	$(CC) $(CFLAGS) -o $@ $< $(LIBS)

clean:
	rm -f *.o *~ $(BINS)
