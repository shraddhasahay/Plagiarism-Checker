
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
import tkinter
from tkinter import *
from PIL import ImageTk
import docx
import os



input_sentence='/0'
pattern_sentence='/0'
in_list=[]
pat_set=set()
hash_in_list=[]
hash_pat_set=set()
plagiarism_dict={}
plagiarism_value=0
output=""
d_name = r'C:\Users\Shraddha Sahay' #enter your document location without document name
suff= '.docx' #doc or docx
#button calls main which inturn calls other functions
def main():
    global input_sentence
    global pattern_sentence
    global in_list
    global pat_set
    global hash_in_list
    global hash_pat_set
    global plagiarism_value
    input_sentence=ment.get()
    pattern_sentence=ment2.get()
    pre_process(input_sentence,1)
    pre_process(pattern_sentence,0)
    my_hash(in_list,1)
    my_hash(pat_set,0)
    find_plagiarism_count(hash_in_list,hash_pat_set)
    calculate_percentage()
    label1 = tkinter.Label(window, text= float(plagiarism_value))
    canvas1.create_window(250, 230, window=label1)

#calculate percentage of plagarism
def calculate_percentage():
    
    global hash_in_list
    global hash_pat_set
    global plagiarism_dict
    global plagiarism_value
    matching_hash=0
    #for _,x in plagiarism_dict.items():
        #matching_hash = matching_hash+x
    matching_hash=len(plagiarism_dict)
    plagiarism_value=(matching_hash*200)/(len(hash_in_list)+len(hash_pat_set))
    
    print("Plagiarism percentage is : {}%".format((matching_hash*200)/(len(hash_in_list)+len(hash_pat_set))))

def data(filename):
    data="\0"
    full_path=os.path.join(d_name,filename+suff)
    doc = docx.Document(full_path)

    all_paras = doc.paragraphs
    for para in all_paras:
        print(para.text)
        print("-------")
        data+=para.text
    return data 
#stemming of input and pattern string
def pre_process(sentence, mode):  
    #sentence -> what to stem
    #mode->0- pattern 1-input_Sent
    final_sent=data(sentence)
    global in_list
    global pat_set
    tokenizer = RegexpTokenizer(r'\w+')
    result = tokenizer.tokenize(final_sent)
    no_punctuation_string=""
    for x in result:
        no_punctuation_string = no_punctuation_string + " "+x
    stop_words = set(stopwords.words('english')) 
    word_tokens = word_tokenize(no_punctuation_string)
    print(word_tokens)
    filtered_sentence = [w for w in word_tokens if not w in stop_words] 
    filtered_sentence = [] 
    for w in word_tokens: 
        if w not in stop_words: 
            filtered_sentence.append(w) 
    stemming=PorterStemmer()
    x=[stemming.stem(w) for w in filtered_sentence]
    if mode==1:

        in_list=list(x)
        print("in_list",in_list)
    elif mode==0:
        pat_set=set(x)
        print("pat_set",pat_set)
    final_sent='/0'
   
#generation of hash values using Rabin Karp method
def my_hash(value,k):
    # value->in_list k=1 store in hash_in_list
    # value->pat_set k=0 store in hash_pat_set
    global hash_in_list
    global hash_pat_set
    l=0
    word=0
    letter=0
    for s in value:
        l=len(s)
        for i in range(0,l):    
            letter=ord(s[i])*pow(7,l-i-1)
            word+=letter
        if k==1:
            hash_in_list.append(word)
            
        elif k==0:
            hash_pat_set.add(word)
            
        word=0
    if k==1:
        pass

        #print("input sentence\n",hash_in_list)
    elif k==0:
        pass
        #print("pattern sentence\n",hash_pat_set)


#create dictionary of key as hash value and value of number of times match
def find_plagiarism_count(hash_in_list,hash_pat_set):
    global plagiarism_dict
    i=1
    for x in hash_pat_set:
        for y in hash_in_list:
            if x==y:
                plagiarism_dict[x]=i
                i+=1
        i=1
    print("plagiarism dictionary",plagiarism_dict)

window=tkinter.Tk()
canvas1 = tkinter.Canvas(window, width = 500, height = 500)
canvas1.pack()
logo = ImageTk.PhotoImage(file=r'C:\Users\Shraddha Sahay\Desktop\bg.png') #for background image in tkinter window
window.title("String plagiarism detector")
label = Label(window, text = "Welcome to Plagiarism detector")
canvas1.create_window(250,10,window=label)
canvas1.create_image(0, 0, image=logo, anchor=NW)
ment=tkinter.StringVar()
ment2=tkinter.StringVar()
label1 = Label(window, text = "Enter (input) file name 1")
canvas1.create_window(85,100,window=label1)
entry1 = tkinter.Entry (window,textvariable=ment) 
canvas1.create_window(320, 100, window=entry1,width="300")
label2 = Label(window, text = "Enter (pattern) file name 2")
canvas1.create_window(90,140,window=label2)
entry2 = tkinter.Entry (window,textvariable=ment2) 
canvas1.create_window(320, 140, window=entry2,width="300")
button1 = tkinter.Button(text='Calculate', command=main)
canvas1.create_window(250, 200, window=button1)
window.mainloop()
