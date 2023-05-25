# colab_starter
run in colab 
[python code]
'''
# run this code in colab cel
######################################################
import os 
os.system('curl https://raw.githubusercontent.com/bxck75/colab_starter/main/setup.py -o /content/setup.py')
from subprocess import Popen, PIPE 
with Popen(["python", "/content/setup.py"], stdout=PIPE) as p: 
    text = p.stdout.read1().decode("utf-8") 
    print(text, end='', flush=True)
######################################################
'''
[\python_code]
