#!/usr/bin/env python

import os
import sys

sys.path.append(os.getcwd() + "/lib")

from notify_recv.cli import CLI

CLI.start()
