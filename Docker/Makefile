CONTAINER_NAME=askfm_scraper

build:
	docker build -t $(CONTAINER_NAME) .

run:
	docker run -p 5001:5000 $(CONTAINER_NAME)
#docker run -it $(CONTAINER_NAME)
#docker run --rm -it $(CONTAINER_NAME)

clean:
	docker rmi -f $(CONTAINER_NAME)
