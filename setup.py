'''
# run this code in colab cel
# import os
# out = os.popen('python /content/setup.py').read()
# print(out)
'''

import os,subprocess

# system functions

def recursive_glob(treeroot, pattern):
  results = []
  for base, dirs, files in os.walk(treeroot):
    goodfiles = fnmatch.filter(files, pattern)
    results.extend(os.path.join(base, f) for f in goodfiles)
  return results

def cmdline(cmd,pr=False):
  result =[]
  f = os.popen(cmd)
  try:
    for line in f:
      if pr == True:
        print(line)
        result.append(line),
  finally:
    f.close()
  return result

def copydir(source_dir,target_dir):
    cmdline('cp -rf '+ source_dir + ' '+ target_dir)

# stinking default folder...poef!
cmdline('rm -r /content/sample_data')
cmdline('pip install gitpython')

# pick filesystem
filesystem = "local" 
if filesystem == 'gdrive':
  # sync google drive
  from google.colab import drive
  import os
  # if drive is needed uncomment
  print('Google drive ',end='')
  drive.mount('/content/drive',force_remount=True)
  print('Root folder set to ',end='')
  root = '/content/drive/My drive/image_learning'
else:
  root = '/content/GitGo'


print('Root folder set to ',end='')
print(root)

#shoot root
os.makedirs(root,exist_ok = True)
os.chdir(root)

# install missing lib
cmdline('pip install theano sklearn imageio tensorflow-gpu==2.0.0-alpha0')
cmdline('apt install tree')
# import the rest
import numpy as np
from PIL import Image
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D,MaxPooling2D
from keras.optimizers import SGD, RMSprop,adam
from keras.utils import np_utils
import  glob, shutil, fnmatch, time, cv2, itertools
from IPython.display import clear_output, display, Image
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
from google.colab.patches import cv2_imshow
import ipywidgets as widgets
from subprocess import PIPE, Popen
# list of reps uncomment to install
reps=[
        'yt-dlp/yt-dlp ',
        'mikf/gallery-dl',
        'bxck75/piss-ant-pix2pix',
        'bxck75/A1_CycleGAN-and-pix2pix_with_colab',
        'bxck75/CartoonGAN-Test-Pytorch-Torch',
        'bxck75/OpenCV-Anime-Face-Detector',
        'tkarras/progressive_growing_of_gans/tree/original-theano-version',
        'willylulu/celeb-hq-modified',
#        'eriklindernoren/Keras-GAN',
#        'keras-team/keras-contrib',
#        'mikf/gallery-dl',
         'bxck75/datasets',
#         'tjwei/Flappy-Turtle.',
#         'tjwei/fonttools',
#         'tjwei/blender3d_import_psk_psa',
         'lllyasviel/sketchKeras',
#         'Mckinsey666/Anime-Face-Dataset',
#         'chenyuntc/pytorch-book',
#         'chenyuntc/PyTorchText',
#         'lllyasviel/style2paints',
#         'llSourcell/GANS-for-style-transfer',
         'opencv/open_model_zoo',
         'opencv/opencv',
         'ultralytics/flickr_scraper',
#         'hindupuravinash/the-gan-zoo',
#         'corenel/GAN-Zoo',
#         'eriklindernoren/Keras-GAN',
         'junyanz/CycleGAN',
#         'junyanz/pytorch-CycleGAN-and-pix2pix',
#         'junyanz/iGAN', #----> !wget http://efrosgans.eecs.berkeley.edu/iGAN/datasets/church_64.zip <----dataset 	outdoor_128.zip 	handbag_128.zip !!!
#         'martinarjovsky/WassersteinGAN',
#         'shaoanlu/faceswap-GAN',
#         'LantaoYu/SeqGAN',
#         'tjwei/GANotebooks',
#         'adeshpande3/Tensorflow-Programs-and-Tutorials',
#         'adeshpande3/Generative-Adversarial-Networks',
#         'diegoalejogm/gans',
         'osh/KerasGAN',
#         'r9y9/gantts',
#         'jayleicn/animeGAN',
#         'jayleicn/ImageNet-Training',
#         'Zardinality/WGAN-tensorflow',
#         'timsainb/Tensorflow-MultiGPU-VAE-GAN',
#         'Larox/python-moviepy-meetup',
#         'tjwei/keras-yolo3',
#         'tensorflow/gan',
#         'tensorflow/moonlight'
#         'tensorflow/models',
#         'tensorflow/datasets',
#         'tensorflow/docs',
#         'tensorflow/text',
#         'mnicnc404/CartoonGan-tensorflow',
#         'Yijunmaverick/CartoonGAN-Test-Pytorch-Torch',
#         'keras-team/keras-contrib',
#         'mnicnc404/CartoonGan-tensorflow',
]



# Gitgo class
class GitGo():
  
  def __init__(self,repos,sub_repos=False,chdir=True,path='/content/'):
    self.sub_repo_list = []
    self.GitUsers=[]
    self.repos = repos
    self.chdir = chdir
    self.path = path
    os.makedirs(self.path, exist_ok = True)
    if 'help' in self.repos:
      self.help()
    self.install_reps()
    self.custom_reps_setup()
    self.install_requirements()
    if sub_repos == True:
      self.get_other_reps()

  def help(self):
    return "* pulls git rep and shows files \
            * returns root path for the repository \
            * Function needs repository / combination\
            * Switch chdir and define the rootpath for the repository\
            * Use : GitGo(, sub_repos=, path=)\
            "
  
  def install_reps(self):    
    for rep in self.repos:
      self.rep=rep.split('/')
      # change folder check
      if self.chdir ==True:
        #Switch to path
        os.chdir(self.path)
      # pull the git repo
      cmdline('git clone https://github.com/'+self.rep[0]+'/'+self.rep[1]+'.git',True)
      # Set the return value for rep rootpath
      self.PATH=self.path+self.rep[1]
    # show imported files
    os.system('ls ' + root)

  def custom_reps_setup(self):
    # custom stuff for CartoonGAN-tensorflow and keras-team/keras-contrib
    if 'keras-team/keras-contrib' in self.repos:
      os.chdir(self.path+'/keras-contrib')
      cmdline('python convert_to_tf_keras.py')
      cmdline('USE_TF_KERAS=1')
      cmdline('python setup.py install')
      import tensorflow as tf
      tf.__version__     
    # custom setup stuff for gallery-dl repo
    if 'mikf/gallery-dl' in self.repos:
      os.chdir(root+'/gallery-dl')
      cmdline("pip install -e . |grep 'succes'",True)
    # custom setup stuff for youtube-dl repo
    if 'yt-dlp/yt-dlp' in self.repos:
      os.chdir(root+'/yt-dlp') 
      cmdline("pip install -e . |grep 'succes'",True)
    if 'tensorflow/text' in self.repos:
      os.chdir(root+'/text')
      cmdline('pip install tensorflow_text==2.0.1')     
    # switch backt to root
    os.chdir(self.path)
  
  def install_requirements(self):
    # install reqs
    loot = recursive_glob(root,'requirements.txt')
    print("[Installing " + str(len(loot)) + " requirements files!]")
    for l in loot:
        print("["+l+"]")
        cmdline('pip install -r ' + l)
        
  def get_other_reps(self):          
      for r in self.repos:
        self.GUSER=r.split('/')[0]
        self.repo_name=r.split('/')[1]
        self.GitUsers.append(self.GUSER)
        gitstr = 'git@[^"]*'
        cmdline("curl https://api.github.com/users/" + self.GUSER + "/repos?per_page=100 | grep -o '"+gitstr+"' > " + os.path.join(root,"info.txt"))
        cmdline('cat '+root+"/info.txt |awk -F ':' '{print $2}'|awk -F '.' '{print $1}' > "+self.path+"/"+self.GUSER+"_repositories.txt",True)
        with open(root+'/info.txt','r') as f:
            for line in f:
              cline=line.split(':')[1].split('.')[0]
              self.sub_repo_list.append(cline),
      
      print("[Installed Repositories]")
      print(self.sub_repo_list)          

      def __repr__(self):
        return self.PATH

# End GitGo Class

#install git reps
G=GitGo(reps,sub_repos=True,path=root)
