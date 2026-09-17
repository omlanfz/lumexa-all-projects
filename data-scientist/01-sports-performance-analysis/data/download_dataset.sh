#!/usr/bin/env bash
# Downloads the real dataset this project uses (too large to ship inside the
# delivery ZIP directly). This is the exact same public, real FiveThirtyEight
# NBA Elo dataset the notebook and lesson materials describe and analyze.
set -e
cd "$(dirname "$0")"
curl -L -o nbaallelo.csv "https://raw.githubusercontent.com/fivethirtyeight/data/master/nba-elo/nbaallelo.csv"
echo "Downloaded nbaallelo.csv ($(wc -l < nbaallelo.csv) lines) into $(pwd)"
