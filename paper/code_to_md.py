#!/usr/bin/env python3

import os
import re

root_dir = "../code"
ignore_dirs = ["../code/backup/.*", "../code/frontend/lib/.*", ".*.png", ".*idea.*", ".*.svg", ".*.md"]
heading_style = "### "
beginning = "## Quellcode\n"


for root, dirs, files in os.walk(root_dir):
    for f in files:
        path = (root + "/" + f)

        ok = True
        for ig_dir in ignore_dirs:
            if re.search(ig_dir, path):
                ok = False

        if ok:
            beginning += heading_style + re.sub(root_dir + "/", "", path) + "\n```\n" + open(path).read() + "\n```\n"

print(beginning)
