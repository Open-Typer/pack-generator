input := $(wildcard configs/*)

all:
	mkdir -p out
	$(foreach name,$(input),python3 generate.py $(name) -o out/$(basename $(notdir $(name)))-A;)
