#!/usr/bin/env python3
import argparse
import subprocess

# CLI arguments.

parser = argparse.ArgumentParser(description='Download all of Hackage. Drops each package into the current directory.')
selection_group = parser.add_mutually_exclusive_group(required=True)
selection_group.add_argument('--latest', action='store_true', help='Download only latest package versions, instead of all versions')
selection_group.add_argument('--all', action='store_true', help='Download only latest package versions, instead of all versions')
args = parser.parse_args()

# Get list of available packages.

cabal_list = "cabal list --simple"
print(cabal_list)
lines = subprocess.check_output([cabal_list], shell=True, universal_newlines=True).strip().split('\n')

# Filter packages.

if args.latest:
  to_download = sorted(dict(l.split() for l in lines).items())
elif args.all:
  to_download = sorted(l.split() for l in lines)
else:
  assert False, "args has neither .latest nor .all, cannot happen"

print("Versions to download: " + str(len(to_download)))

# Write URLs to file.

with open("_urls.txt", "w") as f:
  for name, version in to_download:
    f.write("https://hackage.haskell.org/package/" + name + "/" + name + "-" + version + ".tar.gz\n")

# Download URLs.

xargs = "xargs -P 100 -n 50 wget --quiet < _urls.txt"
print(xargs)
# check=False because some wgets may error (Hackage often gives "410 Gone")
subprocess.run(xargs, shell=True, check=False)

# Unpack.

unpack = "find . -name '*.tar.gz' | xargs -P$(nproc) -I '{}' sh -c 'echo {}; tar -xf {}; rm -f {}'"
print(unpack)
# check=False because some tars extract only with errors (e.g. "gzip: stdin: decompression OK, trailing garbage ignored")
subprocess.run(unpack, shell=True, check=False)
