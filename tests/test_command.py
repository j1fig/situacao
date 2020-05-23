import subprocess

import pytest


@pytest.mark.parametrize("cmd,return_code", [
    (["situacao", "-h"], 0),
    (["situacao"], 2),
])
def test_command(cmd, return_code):
    r = subprocess.run(cmd)
    assert r.returncode == return_code
