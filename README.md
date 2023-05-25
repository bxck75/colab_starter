# colab_starter
run in colab [code]
import os
from subprocess import Popen, PIPE
with Popen(["python", "/content/setup.py"], stdout=PIPE) as p:
    text = p.stdout.read1().decode("utf-8")
    print(text, end='', flush=True)

[\code]
