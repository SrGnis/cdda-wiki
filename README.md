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

After getting the data from the Wayback Machine we need to clean and restructure it to be usable.

The build.sh script will clone the repository in the `.tmp` folder and check out the the commit 3e5ca38ff582623df5630dfa4e8a47d4a6bff28c that has the original data in the web folder.

The next step is tp run the cleaning.py script the will clean and restructure the data in several ways:

    - Delete unwanted root folders

    - Delete files garbage files

    - Rename and move index.html files

    - Remove empty directories

    - Rename files and directories containing "title="

    - Rename non-HTML files in cdda_wiki

    - Move contents of cdda_wiki to the parent directory

    - Remove empty directories again

    - Modify the links to be local friendly

    - Add .html extension to all the html links

    - Rename the files that have a get query name

Finaly the folder .tmp/web replaces the web folder

Just run the scriot with

```
./build.sh
```