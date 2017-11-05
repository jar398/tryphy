#!/usr/bin/python

import argparse, os, time, json

argparser = argparse.ArgumentParser(description='Install a fresh access token, expiring in one hour.')
argparser.add_argument('token')

args = argparser.parse_args()

path = 'config.json'
if not os.path.exists(path):
    path = 'config-template.json'

with open(path, 'r') as infile:
    j = json.load(infile)

j['access_token'] = args.token
# Token expires after one hour
j['access_token_expires'] = time.time() + 3600
with open('config.json.new', 'w') as outfile:
    json.dump(j, outfile, indent=2)
    outfile.write('\n')
os.rename('config.json.new', 'config.json')
