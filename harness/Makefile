all : harness.so

%.so : %.c
	$(CC) -shared -o $@ -fPIC $<
