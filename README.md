## [CSN](http://chiasenhac.vn) downloader

Baby Steps to create a batch chiasenhac downloader from query strings. Feel free to contribute.

Requirements:
  - python3, and a python environment satisfying [these](requirements.txt) requirements.
  - a command line downloader (I have used aria2). Make changes [here](scrap.py#L49).

**Add files folders.txt and queries.txt in the root directory.**

[urls.json](urls.json) is the main configuration file, containing an array of objects, each containing the fields **query**, **url** and **status**.
Urls will appear after downloading, and status will toggle or be set to yes. Best quality music available will be downloaded.

Specify search queries in [queries.txt](queries.txt) separated by newlines.

Specify folders containing music if you want to redownload them in better quality in [folders.txt](folders.txt).

[jsonify_queries.py](jsonify_queries.py) appends the queries in [urls.json](urls.json).

[add_folders.py](add_folders.py) extracts names as queries from the filenames in the folders specified in [folders.txt](folders.txt) and appends them to [urls.json](urls.json). I had songs in the format `album_name_-_song-name.mp3`.

Running [scrap.py](scrap.py) will download music to [downloads](downloads/)