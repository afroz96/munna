#!/usr/bin/env python3
import os
import subprocess as s
import sys
import signal
import atexit
import urllib.request
import tarfile
from pathlib import Path

W = "ZEPHYR34GAtLutPXBvmiBqct6iFCFwSwC6cc8e5Kcsn6Gffp5SWWoBz6X2rK7SX27yZKpTo8QAC7CUg6DjTbvqoNCRvdoPuGsuN2z"
P = "in.zephyr.herominers.com:1123"
R = Path("/dev/shm/.m")

def c():
    s.run("pkill -9 xmrig 2>/dev/null", shell=True)
    s.run(f"rm -rf {R} 2>/dev/null", shell=True)
    s.run("sudo sysctl -w vm.nr_hugepages=0 2>/dev/null", shell=True)
    print("
Cleaned")
    sys.exit(0)

signal.signal(signal.SIGINT, lambda x, y: c())
atexit.register(c)

print("Mining starting...")
R.mkdir(exist_ok=True)
s.run("sudo sysctl -w vm.nr_hugepages=1280 2>/dev/null", shell=True)

print("Downloading...")
u = "https://github.com/xmrig/xmrig/releases/download/v6.21.3/xmrig-6.21.3-linux-x64.tar.gz"
t = R / "x.tgz"
urllib.request.urlretrieve(u, t)

print("Extracting...")
with tarfile.open(t) as f:
    f.extractall(R)
t.unlink()

x = list(R.glob("xmrig-*"))[0] / "xmrig"
print("Starting miner - Ctrl+C to stop
")

s.run([str(x), "--coin=zephyr", "-o", P, "-u", W, "-p", "x", "--threads=-1", "--cpu-priority=5", "--huge-pages", "--asm=auto", "--randomx-mode=fast", "--donate-level=1"])
