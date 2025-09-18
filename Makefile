.PHONY: build-ran build-core
build-ran:
	docker build -t ran-sim:local apps/ran-sim
build-core:
	docker build -t core-sim:local apps/core-sim
