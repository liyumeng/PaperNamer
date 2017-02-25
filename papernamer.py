import os,sys
import re
import numpy as np
from bs4 import BeautifulSoup
import shutil  
import subprocess

if __name__=='__main__':
    print('正在重命名...')
    input_file=sys.argv[1]
    if input_file.endswith('.pdf')==False:
        print('只能处理pdf文件')
        sys.exit(0)
        
    install_path=os.path.dirname(os.path.abspath(__file__))
    tmp_path=os.path.join(install_path,'tmp')
    pdftohtml_path=os.path.join(install_path,'pdftohtml.exe')
    
    if os.path.exists(tmp_path):
        shutil.rmtree(tmp_path)
        
    p = subprocess.Popen([pdftohtml_path,'-q','-l','1',input_file,tmp_path],
            bufsize=2048, stdin=subprocess.PIPE)
    p.wait()
    
    if p.returncode == 0:
        with open(os.path.join(tmp_path,'page1.html'),encoding='utf8') as f:
            html=f.read()

        sizes=re.findall('font-size:(\d+?)px;',html)
        max_size=np.max([int(size) for size in sizes])

        soup=BeautifulSoup(html,'html.parser')

        titles=[]
        for item in soup.find_all('span'):
            style=item.attrs['style']
            if 'font-size:%dpx'%max_size in style:
                titles.append(item)
        new_filename=titles[0].text
        new_filename=new_filename.replace(":","-")
        os.rename(input_file,new_filename+'.pdf')
        print('已重命名为: ',new_filename)
        if os.path.exists(tmp_path):
            shutil.rmtree(tmp_path)
    else:
        print('pdf 读取失败，代码:',p.returncode)

