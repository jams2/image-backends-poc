
# Pluggable image backends POC

## Running the imgproxy POC

1. Set environment variables for imgproxy

	1. `cp .env.example .env`
	2. Set values in `.env` for `IMGPROXY_KEY` and `IMGPROXY_SALT` (`echo $(xxd -g 2 -l 64 -p /dev/random | tr -d '\n')` will do - see [imgproxy docs](https://docs.imgproxy.net/configuration?id=url-signature))

2. Build and run the containers (one for Wagtail, one for imgproxy)

``` shell
export HOSTUID=$(id -u)  # make web container user ID match host user ID
docker-compose up
```

3. Create a superuser

``` shell
docker-compose exec web bash
python manage.py createsuperuser
```

4. [Create an instance of ImageTestingPage](http://localhost:8000/admin/pages/3/add_subpage/), adding some images to the StreamField

5. View your new page
