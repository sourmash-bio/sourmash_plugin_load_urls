"""
Tests for the sourmash load_urls plugin
"""
import os
import pytest

import sourmash
import sourmash_tst_utils as utils
from sourmash_tst_utils import SourmashCommandFailed

# location of remote files - use github for now
remote_loc = 'https://raw.githubusercontent.com/sourmash-bio/sourmash_plugin_load_urls/main/tests/test-data/'


def test_run_sourmash():
    status, out, err = utils.runscript('sourmash', [], fail_ok=True)
    assert status != 0                    # no args provided, ok ;)


def test_load_sig_http():
    # test remote loading of a signature file
    url47 = remote_loc + '47.fa.sig'
    sig47 = utils.get_test_data('47.fa.sig')

    remote_idx = sourmash.load_file_as_index(url47)
    assert len(remote_idx) == 1
    siglist = list(remote_idx.signatures())
    remote_sig = siglist[0]

    local_idx = sourmash.load_file_as_index(sig47)
    assert len(local_idx) == 1
    siglist = list(local_idx.signatures())
    local_sig = siglist[0]

    assert local_sig == remote_sig


def test_load_manifest():
    # test remote loading of a CSV manifest
    mf_url = remote_loc + 'a-manifest.csv'

    remote_idx = sourmash.load_file_as_index(mf_url)
    assert len(remote_idx) == 2

    sig47 = utils.get_test_data('47.fa.sig')
    sig63 = utils.get_test_data('63.fa.sig')

    ss47 = list(sourmash.load_file_as_signatures(sig47))[0]
    ss63 = list(sourmash.load_file_as_signatures(sig63))[0]

    assert ss47 in remote_idx.signatures()
    assert ss63 in remote_idx.signatures()
