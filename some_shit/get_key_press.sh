xinput list |   grep -Po 'id=\K\d+(?=.*slave\s*keyboard)' |   xargs -P0 -n1 xinput test
