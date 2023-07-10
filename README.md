
# Pluggable image backends POC

## Setting up imgproxy

1. Set environment variables for imgproxy

	1. `cp .env.example .env`
	2. Set values in `.env` for `IMGPROXY_KEY` and `IMGPROXY_SALT` (`echo $(xxd -g 2 -l 64 -p /dev/random | tr -d '\n')` will do - see [imgproxy docs](https://docs.imgproxy.net/configuration?id=url-signature))


## Setting up imgix

1. Set up a free account on [imgix](https://imgix.com)
2. Follow the [quick-start guide](https://docs.imgix.com/setup/quick-start)
   - use any appropriate name for your subdomain
   - select "web proxy" for your storage location
3. Add `IMGIX_DOMAIN` to your .env (e.g. `pluggable-rendition-backends.imgix.net`)
3. Take a note of your imgix signature key - this can be retrieved by revealing the "token" in the security section of the dashboard for your source
   - add `IMGIX_SIGNATURE_KEY` to your .env, with this value


## Running the application

1. Run a reverse proxy targeting port 8000 on your machine, e.g. with ngrok. This is necessary as imgix is a hosted service and needs to query your local application server for the original rendition
2. Build and run the containers (one for Wagtail, one for imgproxy)

``` shell
export HOSTUID=$(id -u)  # make web container user ID match host user ID
export PROXY_URL_FOR_IMGIX='e.g. your ngrok URL'
docker-compose up
```

3. Create a superuser

``` shell
docker-compose exec web bash
python manage.py createsuperuser
```

4. [Create an instance of ImageTestingPage](http://localhost:8000/admin/pages/3/add_subpage/), adding some images to the StreamField

5. View your new page
