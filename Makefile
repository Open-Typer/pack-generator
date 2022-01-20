input := $(wildcard configs/*.conf)

all:
	mkdir -p out
	$(foreach name,$(input),python3 generate.py $(name) -w configs/$(basename $(notdir $(name)))_wordlist.txt -o out/$(basename $(notdir $(name)))-A;)
