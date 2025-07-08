help:
		@echo make run
		@echo make clean


run:
	uv run main.py

clean:
	rm -fr ./output
