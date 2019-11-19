import re
import os.path
import os


#Project path
path = "C:/Users/pg540/Desktop/Cour/M1/Projet TAL"
#Path of txt article directory
path_txt = "C:/Users/pg540/Desktop/Cour/M1/Projet TAL/Corpus/txt"
#Destination Path for Cleaned txt article
path_article =  "C:/Users/pg540/Desktop/Cour/M1/Projet TAL/Corpus/article_txt"
#Destination Path for extracted abstract 
path_abstract = "C:/Users/pg540/Desktop/Cour/M1/Projet TAL/Corpus/abstract_txt"

def get_file_number(path):
	num_files = len([f for f in os.listdir(path)if os.path.isfile(os.path.join(path, f))])
	print("file number : " + str(num_files))
	return num_files

def clean_txt():
	f = open("A80.txt", "r", errors="ignore")
	txt = f.read()
	#print(txt)
	print(re.sub('[^\w\s.,]', '*', txt))

	f.close
	return txt

def create_directory():
	ppatch = path + "/Corpus"
	if not os.path.exists(ppath):
		os.makedirs(ppath)
	if not os.path.exists(ppath + "/txt"):
		os.makedirs(ppath + "/txt")
	if not os.path.exists(ppath + "/art"):
		os.makedirs(ppath + "/art")
	if not os.path.exists(ppath + "/ "):
		os.makedirs(ppath + "/ ")

def delete_abstract(txt, abstract):
	txt.replace(abstract, " ")


def extract_abstract(path):
	f = open(path, "r", errors="ignore")
	txt = f.read()
	#delete all \n
	txt = re.sub('\\n', ' ',txt)
	result = re.search('[Aa ][Bb][Ss][Tt][Rr][Aa][Cc][Tt].([\s\S]*?).[Ii ][Nn][Tt][Rr][Oo][Dd][Uu][Cc][Tt][Ii][Oo][Nn]', txt)	
	#result = re.search('Abstract(.*)Introduction', txt)
	if result is not None:
		abstract = result.group(1)
	else:
		abstract="error"
	#print(result)
	f.close
	return str(abstract)

def separte_abstract_artcile(tpath):
	#txt cleaning
	txt = clean(tpath)
	#f = open(tpath, "r", errors="ignore")
	#txt = f.read()
	#delete all \n
	#og_txt = re.sub('\\n', ' ',txt)
	og_txt = txt
	#get abstract
	result = re.search('[Aa ][Bb][Ss][Tt][Rr][Aa][Cc][Tt]([\s\S]*?)\d*\s*[Ii ][Nn][Tt][Rr][Oo][Dd][Uu][Cc][Tt][Ii][Oo][Nn]', og_txt)
	if result is None:
		with open('C:/Users/pg540/Desktop/Cour/M1/Projet TAL/Corpus/Extract_Error.txt', 'a') as g:
			g.write(tpath + "\n")
			g.close()
			abstract = "******"
	else:
		abstract = result.group(1)
	article = re.sub('[Aa ][Bb][Ss][Tt][Rr][Aa][Cc][Tt]([\s\S]*?)[Ii ][Nn][Tt][Rr][Oo][Dd][Uu][Cc][Tt][Ii][Oo][Nn]', '******', og_txt)
	#f.close()

	return abstract, article


def create_txt_file(path,s):
		file = open(path, "w")
		file.write(s)
		file.close

def run(txt_path, article_path, abstract_path):
		nb = get_file_number(txt_path)
		#loop on all the txt file
		for i in range(nb):
			abstract,article = separte_abstract_artcile(txt_path + "/A" + str(i+1) + ".txt")
			print("--A" + str(i+1))
			print("abstract len : "+ str(len(abstract)))
			print("article len : "+ str(len(article)))
			if len(abstract) > 2200 or len(abstract) < 200:
				create_txt_file(path+"/Corpus/problem" + "/A" + str(i+1) + "_abstract_ER.txt", abstract)
				create_txt_file(path+"/Corpus/problem" + "/A" + str(i+1) + "_article_ER.txt", article)
				print("ERROR")
			else:
				create_txt_file(abstract_path + "/A" + str(i+1) + "_abstract.txt", abstract)
				create_txt_file(article_path + "/A" + str(i+1) + "_article.txt", article)

			#abstract = extract_abstract(txt_path + "/A" + str(i+1) + ".txt")
			#create_txt_file(abstract_path + "/A" + str(i+1) + "_abstract.txt",abstract)

			#get txt without abstract
			



def Clean_ref(txt_path):
	nb = get_file_number(txt_path)
	print(nb)
	
		#loop on all the txt file
	for i in range(2):
		print(str(i+1))
		f = open(txt_path + "/A" + str(i+1) + ".txt", "r+", errors="ignore")
		txt = f.read()
		#delete Reference part
		result = re.sub('R[Ee][Ff][Ee][Rr][Ee][Nn][Cc][Ee][\s\S]*'," ",txt)
		#delete web URL
		result2 = re.sub('(https[^\s]+)',"*",result)
		#delete weird charachter
		result3 = re.sub('[^a-zA-Z0-9\s\(\)\[\]\-,’;:.\/!\?]'," ",txt)
		f.write(result2)
		

def clean(txt_path):
	f = open(txt_path, "r", errors="ignore")
	txt = f.read()
	#delete Reference part
	result = re.sub('R\s{0,1}[Ee][Ff][Ee][Rr][Ee][Nn][Cc][Ee][\s\S]*'," ",txt)
	#delete web URL
	result2 = re.sub('(https[^\s]+)'," ",result)
	#delete weird charachter
	result3 = re.sub('[^a-zA-Z0-9\s\(\)\[\]\-,’;:.\/!\?]'," ",result2)
	f.close()
	return result3	

#[Aa ][Bb][Ss][Tt][Rr][Aa][Cc][Tt]([\s\S]*)[Ii ][Nn][Tt][Rr][Oo][Dd][Uu][Cc][Tt][Ii][Oo][Nn]
#print(re.sub('Reference([\s\S]*)', '*', txt))

#[^a-zA-Z0-9ÀÂÇÈÉÊËÎÔÙÛàâçèéêëîôùû\s\(\)\[\]"'\-,;:\/!\?]

#a,b = separte_abstract_artcile(path_txt+"/A10.txt")
#print(a)

f = open(path_txt + "/A48"  + ".txt", "r", errors="ignore")
txt = f.read()
print(txt)
result = re.findall("^.{1,5}\n", txt, re.MULTILINE)
print(result)

#run(path_txt,path_article,path_abstract)

