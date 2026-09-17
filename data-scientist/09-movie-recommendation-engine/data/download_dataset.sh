#!/usr/bin/env bash
# Downloads ratings.csv (too large to ship inside the delivery ZIP directly).
# This is the exact same real MovieLens ratings file the training script and
# README describe (1,000,209 real ratings from 6,040 users).
set -e
cd "$(dirname "$0")"
curl -L -o ratings.csv "https://raw.githubusercontent.com/khanhnamle1994/movielens/master/ratings.csv"
echo "Downloaded ratings.csv ($(wc -l < ratings.csv) lines) into $(pwd)"
