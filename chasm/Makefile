CC=bun
BUNARGS=build --compile --minify --sourcemap
SRC=src/index.tsx
OUT=chasm

all: $(OUT)

$(OUT): $(SRC)
	$(CC) $(BUNARGS) $(SRC) --outfile $(OUT)

.PHONY: clean

clean:
	rm -f $(OUT)

install:
	mkdir -p ~/.local/bun
	cp $(OUT) ~/.local/bin/chasm
