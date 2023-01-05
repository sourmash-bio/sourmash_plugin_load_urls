# sourmash plugin to load files from URLs with fsspec.

This is an **experimental** plugin to support loading signature files
from URLs/URIs with fsspec.

Links:
* [sourmash: sourmash-bio/sourmash/](https://github.com/sourmash-bio/sourmash/)
* [fsspec](https://filesystem-spec.readthedocs.io/en/latest/index.html)

Note: Depends on
[sourmash#2428](https://github.com/sourmash-bio/sourmash/pull/2428).

## Usage

```
pip install .
```

and then you can go on your merry way to load URLs/URIs!

## Supported URL schemas and examples

The underlying
[fsspec package](https://filesystem-spec.readthedocs.io/en/latest/intro.html)
supports [many different types of URIs](https://filesystem-spec.readthedocs.io/en/latest/api.html#built-in-implementations) - for example, you can load from any publicly accessible HTTP/HTTPS URL:

```
sourmash sig describe https://raw.githubusercontent.com/sourmash-bio/sourmash_plugin_load_urls/main/tests/test-data/47.fa.sig
```

You can also load directly from GitHub with the `github://` schema:
```
sourmash sig describe github://sourmash-bio:sourmash_plugin_load_urls@/tests/test-data/47.fa.sig
```

And you can use SSH URIs, but they do require authentication of course ;).
```
sourmash sig describe ssh://ctbrown@farm.cse.ucdavis.edu/home/ctbrown/sourmash/tests/test-data/47.fa.sig
```

## Loading manifests

The `load_urls` plugin will also load CSV manifests from URIs. [`a-manifest.csv`](https://raw.githubusercontent.com/sourmash-bio/sourmash_plugin_load_urls/main/tests/test-data/a-manifest.csv) is an example manifest that you can load like so:

```
sourmash sig describe github://sourmash-bio:sourmash_plugin_load_urls@/tests/test-data/a-manifest.csv
```

If you have multiple remote signatures and you want to load them as a
collection, you can build a manifest that lists them by using
`sourmash sig collect`, and then post the output CSV file somewhere
accessible

For example,
```
sourmash sig collect -o remote-mf.csv -F csv https://raw.githubusercontent.com/sourmash-bio/sourmash_plugin_load_urls/main/tests/test-data/{47,63}.fa.sig
```
will produce the equivalent file to `a-manifest.csv` above.

**TANSTAAFL Warning:** Many operations on manifests will load every
signature listed in the manifest, which can incur a lot of network
traffic (and be very slow).  Remote manifests are probably _most_
useful for small collections or for situations where you are _always_
subsetting or searching the manifest with mechiansms like `--include`,
picklists, and `sig grep`.  Ask about your use case
[on the sourmash issue tracker](https://github.com/dib-lab/sourmash/issues)
and we will try to guide you appropriately!

So, for example, `sig describe` will load every signature:
```
sourmash sig describe github://sourmash-bio:sourmash_plugin_load_urls@/tests/test-data/a-manifest.csv
```
while `sig summarize` just loads the manifest and not the individual
signatures:
```
sourmash sig describe github://sourmash-bio:sourmash_plugin_load_urls@/tests/test-data/a-manifest.csv
```
and `sig grep` loads only matching signatures:
```
sourmash sig grep -c NC_011663.1 github://sourmash-bio:sourmash_plugin_load_urls@/tests/test-data/a-manifest.csv 
```
and you could also select and search only the one match with `sourmash search`:
```
sourmash search <query.sig> --include NC_011663.1 github://sourmash-bio:sourmash_plugin_load_urls@/tests/test-data/a-manifest.csv
```
