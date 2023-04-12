project = nao1986
image = pyjmeter
version = 0.0.1
cache = False

build:
	docker build --no-cache=${cache} \
		--tag ${project}/${image}:${version} \
		--progress plain \
		.

push:
	docker push ${project}/${image}:${version}

