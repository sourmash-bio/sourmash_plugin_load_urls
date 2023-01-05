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
