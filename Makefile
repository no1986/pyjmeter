image = pyjmeter
version = 0.0.1
cache = False

build:
	sudo docker build --no-cache=${cache} \
		--tag ${image}:${version} \
		--progress plain \
		.
