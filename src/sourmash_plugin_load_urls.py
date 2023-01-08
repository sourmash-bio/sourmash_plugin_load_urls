"Read sketches with fsspec."
import sourmash
import fsspec
from sourmash.index import LinearIndex, MultiIndex, StandaloneManifestIndex
from sourmash.manifest import BaseCollectionManifest
import traceback

# CTB: support file lists, CSV files?

###

# @CTB: figure out parent/prefix stuff?

def load_sketches(location, *args, **kwargs):
    of = fsspec.open(location, 'rb')

    try:
        with of as fp:
            # load JSON if we can -
            lidx = LinearIndex.load(fp, filename=location)

            # and then pass into MultiIndex to generate a manifest.
            db = MultiIndex.load((lidx,), (None,), parent=None)

            return db
    except (IOError, sourmash.exceptions.SourmashError):
        pass

    # if we can't read it as a JSON signature, try it as a manifest.
    # CTB: not sure why we can't keep it open in the above block and
    # then do a seek here? But anyway...

    of = fsspec.open(location, 'rt')
    with of as fp:
        mf = BaseCollectionManifest.load_from_csv(fp)
        return StandaloneManifestIndex(mf, location, prefix='')


# default priority is ok here
#load_sketches.priority = 5
