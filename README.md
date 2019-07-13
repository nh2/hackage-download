# hackage-download - Download all of [Hackage](https://hackage.haskell.org)

Script to download all of Hackage. Either `--latest` versions or `--all` historical versions.


## Usage

```
./hackage-download.py --latest
```

```
./hackage-download.py --all
```

Both drop each package into the current directory.


## Performance

`./hackage-download.py --latest` finishes in 77 seconds on my desktop with Gigabit Internet.

* 13 seconds are `cabal list --simple`
* 10 seconds is the downloading of 13981 latest `.tar.gz` packages (900 MB)
* 54 seconds is the un-gzipping on my spinning disk (4.4 GB)


## Interesting facts

### `cabal get` is insanely slow

**80x slower** than my parallel `wget`:

```
cabal list --simple | cut -d' ' -f1 | sort -u | parallel -j100 --load 10 cabal get {}
12535.05s user 566.04s system 276% cpu 1:19:03.51 total
```

This is with `cabal 2.2.0.0`.


### Minimalist one-liner

Downloading latest packages, with GNU `parallel` to render a progress bar:

```
cabal list --simple | python3 -c 'from fileinput import *; [print("https://hackage.haskell.org/package/"+p+"/"+p+"-"+ver+".tar.gz") for (p,ver) in sorted(dict(map(str.split, input())).items())]' | time parallel --bar -P 100 -n 32 wget --quiet {}
```


### Some packages mess with you

* Some packages from `cabal list --simple` fail to download from Hackage, e.g. with `410 Gone` or other errors.
* Some `.tar.gz` packages set funny permissions on the unpacked files which makes removing them a bit of a nuisance.
* Some `.tar.gz` packages have "trailing garbage", resulting in decrompression warnings.
* As a result, the script must do lenient error handling, and will not report correctly on e.g. disk write errors.
