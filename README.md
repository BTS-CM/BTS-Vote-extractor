BTS Vote extractor

To extract all tx, it takes approx 23 days.. so batch/parrallel processing is neccessary. Time to find out if any of the full nodes rate limit...

## Prerequisites

### Python packages

* pip3
* ujson
* bitshares
* progressbar33
* sys

### System

* Tested on Ubuntu 17.10
* Uses Python 3.
* Screen (for multiple workers)

## Usage guide

python3 dump.py scrape_from_value scape_to_value

`example: python3 dump.py 1 100`

Output is a single json file named 'vote_data_*_*.json' where * is the from/to int range values.

One could run many instances of this script at the one time, until you hit a rate limit. Should reduce the dump time from 22 days to 1 day with 22 workers.