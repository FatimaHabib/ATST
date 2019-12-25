import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re
import tarfile
import glob

#Url where to download
url="https://arxiv.org/list/cs/18?skip=7500&show=1000"
#floder where to put downloaded files
path = "C:/Users/pg540/Desktop/Cour/M1/ProjetTAL/NewCorpus/"

#https://arxiv.org/list/cs/1901?skip=2000&show=2000

#Download all the spectific type file from an Url
def Download_from_url():
        x=1
        response = requests.get(url)    
        soup = BeautifulSoup(response.text, "html.parser")
        l = re.findall("format\/(.*?)\"",str(soup))
        for i in l:
                x=x+1
                u = "https://arxiv.org/e-print/" + str(i)
                print(u)
                print("Downloading.....")
                r = requests.get(u)
                #write the files
                with open("D:/Tar_file/" + str(i) + ".tar.gz",'wb') as f:
                        print("writing.....")
                        f.write(r.content)
                f.close()
                print("Done")
        

#extract the LaTex file from the tar.gz file
def untar():
        f = open("C:/Users/pg540/Desktop/Cour/M1/ProjetTAL/NewCorpus/noLatex.txt","a")
        pattern = re.compile(".*\.tex")
        x = 0
        for files in os.listdir("C:/Users/pg540/Desktop/Cour/M1/ProjetTAL/NewCorpus/compressed_raw_files/"):
                #print(files)
                ct = 0
                main = None
                #try to open, avoid corrupted files
                try:
                        t = tarfile.open("C:/Users/pg540/Desktop/Cour/M1/ProjetTAL/NewCorpus/compressed_raw_files/"+files, 'r')
                        #parcour files in the .tar
                        for member in t.getmembers():
                                #Detect .tex files and count them ( 1 is ok, more is problematic (try to take main.tex in this case))
                                if pattern.match(member.name) is not None:
                                        #tex file counter
                                        ct+=1
                                        m = member
                                        if member.name == "main.tex":
                                                main = member
                        #if there is only one, we extract it       
                        if ct ==1:
                                x+=1
                                m.name = "A_Latex_" + str(x) + ".txt"
                                t.extract(m, "C:/Users/pg540/Desktop/Cour/M1/ProjetTAL/NewCorpus/Latex_txt/")
                        #else 
                        else:
                                if main is not None:
                                        x+=1
                                        main.name = "A_Latex_" + str(x) + ".txt"
                                        t.extract(main, "C:/Users/pg540/Desktop/Cour/M1/ProjetTAL/NewCorpus/Latex_txt/")
                                else:
                                        f.write(files + "\n")
                        t.close()


                except:
                        print(files + " is Corrupted!" + "(" + str(os.path.getsize("C:/Users/pg540/Desktop/Cour/M1/ProjetTAL/NewCorpus/compressed_raw_files/"+files)/1000) + ")")
                        f.write(files + " is Corrupted!" + "(" + str(os.path.getsize("C:/Users/pg540/Desktop/Cour/M1/ProjetTAL/NewCorpus/compressed_raw_files/"+files)/1000) + ")")
                        #os.remove("D:/Tar_file/"+files)
        f.close()

#clean the latex file
def clean(txt):
        #remove abstract part
        r = re.sub(r'(\\begin{abstract}[\s\S]*\\end{abstract}?)',"", txt)
        #Remove tables part
        r1 = re.sub(r'\\begin{table}[\s\S]*?\\end{table}',"", r)
        r2 = re.sub(r'\\begin{align}[\s\S]*?\\end{align}',"", r1)
        r3 = re.sub(r'\\begin{subequations[\s\S]*?\\end{subequations}',"", r2)
        r4 = re.sub(r'\\begin{algorithm[\s\S]*?\\end{algorithm}',"", r3)
        #Remove figures part
        r5 = re.sub(r'\\begin{figure}[\s\S]*?\\end{figure}',"" , r4)
        #Remove remove equations part and other things
        r6 = re.sub(r'\\begin{equation}[\s\S]*?\\end{equation}',"" , r5)
        r7 = re.sub(r'\\begin{proof}[\s\S]*?\\end{proof}',"" , r6)
        r8 = re.sub(r'\\begin{abstract}[\s\S]*?\\end{abstract}',"" , r7)
        r9 = re.sub(r'\\begin{theorem}[\s\S]*?\\end{theorem}',"" , r8)
        r10 = re.sub(r'\\begin{eqnarray*}[\s\S]*?\\end{eqnarray*}',"" , r9)
        r11 = re.sub(r'\\begin{eqnarray}[\s\S]*?\\end{eqnarray}',"" , r10)
        r12 = re.sub(r'\\begin{table*}[\s\S]*?\\end{table*}',"" , r11)
        r13 = re.sub(r'\\begin{tabular}[\s\S]*?\\end{tabular}',"" , r12)
        r14 = re.sub(r'\\begin{math}[\s\S]*?\\end{math}',"" , r13)
        r15 = re.sub(r'\\begin{tabbing}[\s\S]*?\\end{tabbing}',"" , r14)
        r16 = re.sub(r'\\begin{equation*}[\s\S]*?\\end{equation*}',"" , r15)
        r17 = re.sub(r'\\begin{align*}[\s\S]*?\\end{align*}',"" , r16)
        r18 = re.sub(r'\\bibitem{[\s\S]*?\n\n',"" , r17)
        r19 = re.sub(r'\\\[[\s\S]*?\\]',"" , r18)
        #Remove all the comments
        r20 = re.sub(r'\%.*\n',"",r19)
        #Remove all the section bornes & $ $ born
        r21= re.sub(r'\$.+?\$',"",r20)
        r22 = re.sub(r'\{.+?\}',"",r21)
     #   print(re.findall(r'\{.+?\}',r12))
        #r12 = re.sub(r'\\.+?\}',"",r11)
        #Remove 
     #   print("\n\n\n\n")
        
     #   print(re.findall(r'\\.*?\s',r13))
        
        r23 = re.sub(r'\\.*?\s',"",r22)
        #r15 = re.sub(r'\n\n',"",r14)
        
        return r23    

#extract the abstract part
def extract(txt):
        result = re.search(r'\\begin{abstract}([\s\S]*?)\\end{abstract}', txt)
        if result is not None:
                abstract = result.group(1)
        else:
                abstract="error"
        print("ab len : " + str(len(abstract)))
        return abstract

def run():
        e = open("C:/Users/pg540/Desktop/Cour/M1/ProjetTAL/NewCorpus/noAbstract.txt","a")
        i=0
        for file in os.listdir("C:/Users/pg540/Desktop/Cour/M1/ProjetTAL/NewCorpus/latex_txt/"):
                f = open("C:/Users/pg540/Desktop/Cour/M1/ProjetTAL/NewCorpus/latex_txt/" + file, "r", errors="ignore")
                txt = f.read()
                print(file)
                i = re.findall('\d+', file)
                print(i)
                abstract = extract(txt)
                clean_txt = clean(txt)
                clean_ab = clean(abstract)
                f.close()
                if len(abstract) < 20:
                        print("no abstract")
                        e.write(file+"\n")
                else:
                        #write article
                        f = open("C:/Users/pg540/Desktop/Cour/M1/ProjetTAL/NewCorpus/article_txt/A_article_" + i[0] + ".txt", "w")
                        f.write(clean_txt)
                        f.close()
                        #if os.path.getsize("C:/Users/pg540/Desktop/Cour/M1/ProjetTAL/NewCorpus/article_txt/A_article_" + i[0] + ".txt") > 2000:
                        #write abstract
                        f = open("C:/Users/pg540/Desktop/Cour/M1/ProjetTAL/NewCorpus/abstract_txt/A_abstract_" + i[0] + ".txt", "w")
                        f.write(clean_ab)
                        f.close()
        e.close()
                
def test():
        f = open("C:/Users/pg540/Desktop/Cour/M1/ProjetTAL/NewCorpus/Latex_txt/A_Latex_93.txt", "r", errors="ignore")
        txt = f.read()
        a = clean(txt)
        print(len(a))
        f = open("C:/Users/pg540/Desktop/Cour/M1/ProjetTAL/NewCorpus/test_clean_txt.txt", "w")
        f.write(a)
        f.close()

def a():
        print(os.path.getsize("C:/Users/pg540/Desktop/Cour/M1/ProjetTAL/NewCorpus/article_txt/A_article_922.txt"))
        
if __name__ == '__main__':
        #a()
        run()
        #test()
        #untar()

