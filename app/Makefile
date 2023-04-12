registry = 10.0.100.112:5000
project = jmeter
image = jmx
version = 0.0.1
cache = False

build:
	sudo docker build \
		--no-cache=${cache} \
		--tag ${registry}/${project}/${image}:${version} \
		.

push:
	sudo docker push \
		${registry}/${project}/${image}:${version}

