import os

script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_directory)
def load_one_file(filename):
    x=[]
    with open(filename,encoding='utf8') as f:
        return [i.strip() for i in f.readlines()]    
    # return x
def load_files_from_dir(rootdir):
    x=[]
    list = os.listdir(rootdir)
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        if os.path.isfile(path):
            if path.endswith('.txt'):
                v=load_one_file(path)
                x+=v
    return x

x = load_files_from_dir('SuperWordList-master')
data =set()
for i in x:
    i = i.strip()
    if '\t' in i:
        data.add(i.split('\t')[0])
        data.add(i.split('\t')[1])
    elif ':' in i:
        data.add(i.split(':')[0])
        data.add(i.split(':')[1])
    else:
        data.add(i)

with open('../weak.txt','w',encoding='utf8') as f:
    for i in data:
        f.write(i+'\n')
    f.close()