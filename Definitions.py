import os,platform

#PAPER_DIR = '/media/sf_Shared/Basket_Papers/Basket_Papers/misq/2017/3/1'
PAPER_DIR = '/media/sf_Shared/Basket_Papers/Basket_Papers/misq/2017/3'
#PAPER_DIR = 'S:\\VMs\\Shared\\Basket_Papers\\Basket_Papers\\isr\\2014\\12\\3'
CODES_PATH = '/media/sf_Shared/Codes_Original.txt'
OS_NAME = platform.system()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Activate lemmatization
LEM = True
# Activate stopword removal
STOP = False