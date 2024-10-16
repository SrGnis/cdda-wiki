# CDDA WIKI

This repo contains the contents of the defunct CDDA Wiki cddawiki.chezzo.com

The contents have been retrived from the [Internet Archive](https://archive.org/) project [The Wayback Machine](https://wayback.archive.org/)

[Support the Internet Archive](https://www.paypal.com/paypalme/internetarchive)

## How?

We used the [wayback-machine-downloader](https://github.com/hartator/wayback-machine-downloader) to download the contents from the Wayback Machine at the date 2024-03-24, more specifically, we used [this fork](https://github.com/ShiftaDeband/wayback-machine-downloader)

Build the Dockerfile with:

```bash
docker build . -t wayback_machine_downloader
```

And start the download with this command:

```bash 
docker run --rm -v ./web:/web wayback_machine_downloader https://cddawiki.chezzo.com -d /web -t 20240324103752
```
