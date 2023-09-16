# 99 Acres Data Scraper

## Overview

This GitHub repository contains a Python project that scrapes data from the 99 Acres website for various cities. The scraped data includes property names,
links, available types of properties, and their respective costs. The project also includes a cron job that runs the scraping script twice a day.

## Features

- Scrapes data from 99 Acres for multiple cities.
- Extracts property names, links, available property types, and their costs.
- Includes a cron job for automated data scraping.
- Easily add requirements using `pip install -r requirements.txt`.
- Run the server with `python manage.py runserver`.
- Run the scraping script manually using `python manage.py scraping_script`.
- MongoDB URI provided in `mongo_uri.txt` for data storage.

## Prerequisites

Before running the project, ensure you have the following:

- Python 3.x installed on your system.
- MongoDB installed and configured (if you wish to use a database).
- Make sure you have the required Python packages installed by running:

```
pip install -r requirements.txt
```

## Running the Project

1. Start the server:

```
python manage.py runserver
```

2. Run the scraping script:

```
python manage.py scraping_script
```

3. Add the cron job to automate the scraping:

```
python manage.py crontab add
```

The cron job is now set up to run the scraping script twice a day.

## Configuration

- The MongoDB URI for data storage can be found in `mongo_uri.txt`.
- You can configure the list of cities and other parameters in the scraping script file.



## Acknowledgments

- The scraping script is based on the 99 Acres website.
- Special thanks to the open-source community for their contributions.

Feel free to contribute to this project and improve the data scraping capabilities or add more features!
