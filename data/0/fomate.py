import os
script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_directory)

def load_one_file(filename):
    x=[]
    with open(filename,encoding='utf8') as f:
        return f.readlines()[0].split()    
    # return x
def load_files_from_dir(rootdir):
    x=[]
    list = os.listdir(rootdir)
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        if os.path.isfile(path) and path.endswith('.txt'):
                print(path)
                v=load_one_file(path)
                x+=v
    return set(x)

x = load_files_from_dir('.')

with open('../normal.txt','w',encoding='utf8') as f:
    for i in x:
        f.write(i+'\n')