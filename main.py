import pandas as pd
import matplotlib.pyplot as plt
import urllib.request
from gensim.models.word2vec import Word2Vec
from konlpy.tag import Okt

from tqdm import tqdm

import csv
import tkinter as tk
import tkinter.font as font

def keyboardHandler(event):
    
    #print(event.keycode)
    
    if(event.keycode==36):
        
        str1 = entry.get()
    
        entry.delete(0, "end")
        
        listbox2.delete(0, "end")
        
        for i in range(0,10):
            listbox2.insert(i," " + model.wv.most_similar(str1)[i][0])


#urllib.request.urlretrieve("https://raw.githubusercontent.com/e9t/nsmc/master/ratings.txt", filename="ratings.txt")

train_data = pd.read_table('ratings.txt')

print(train_data[:5])

print(len(train_data))

print(train_data.isnull().values.any())

train_data = train_data.dropna(how='any')
print(train_data.isnull().values.any())

print(len(train_data))

train_data['document'] = train_data['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")
#train_data['document'] = train_data['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")
print(train_data[:5])

stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']

okt = Okt()

'''
tokenized_data = []
for sentence in tqdm(train_data['document']):
    tokenized_sentence = okt.morphs(sentence, stem=True)
    stopwords_removed_sentence = [word for word in tokenized_sentence if not word in stopwords]
    tokenized_data.append(stopwords_removed_sentence)
    
'''
    
tokenized_data = []
adding = []
    
with open('total.csv', 'r', encoding='utf-8') as f:
    rdr = csv.reader(f)
    for i, line in enumerate(rdr):
        if i==0:
            for ex in line:
                tokenized_data.append(eval(ex))
        elif i==1:
            for ex in line:
                adding.append(ex)
    
'''print('리뷰의 최대 길이:',max(len(review) for review in tokenized_data))
print('리뷰의 평균 길이 :',sum(map(len, tokenized_data))/len(tokenized_data))
plt.hist([len(review) for review in tokenized_data], bins=50)
plt.xlabel('length of samples')
plt.ylabel('number of samples')
plt.show()'''

'''new_tokenized_data = []
for sentence in tokenized_data:
    new_sentence = eval(sentence)
    new_tokenized_data.append(new_sentence)'''

model = Word2Vec(sentences = tokenized_data, vector_size = 100, window = 5, min_count = 5, workers = 4, sg = 0)



print(model.wv.vectors.shape)

window = tk.Tk()
window.title('word2vec')
window.geometry('500x500+500+150')
window.resizable(False,False)

window.bind("<KeyPress>", keyboardHandler)

#myfont = font.Font(family='Segoe UI', size=9, weight='bold', slant='roman', underline=0, overstrike=0)


frame1 = tk.Frame(width=500, height=100, relief='solid',bd=2, bg='red')
frame2 = tk.Frame(width=320, height=400, relief='solid',bd=2, bg='green')
frame3 = tk.Frame(width=180, height=400, relief='solid',bd=2, bg='blue')

'''frame1.place(x=0,y=0)
frame2.place(x=0,y=100)
frame3.place(x=320,y=100)'''
frame1.pack()
frame2.place(x=0,y=100)
frame3.place(x=320,y=100)

label=tk.Label(frame1,text=" 유사도 검색 단어 입력", anchor='center', relief='groove')
#label.config(font=('', 15))
label.pack()

def button_handler():
    str1 = entry.get()
    
    entry.delete(0, "end")
    
    listbox2.delete(0, "end")
    
    for i in range(0,10):
        listbox2.insert(i," " + model.wv.most_similar(str1)[i][0])


entry=tk.Entry(frame1,)
#entry.config(font=('', 15))
entry.pack(side='top',fill='x', expand=1)

button=tk.Button(frame1,text=' 확인', command=button_handler)
#button.config(font=('', 15))
button.pack(side='top',fill='x', expand=1)

scrollbar = tk.Scrollbar(master=frame2, orient='vertical')

listbox = tk.Listbox(master=frame2, yscrollcommand=scrollbar.set)
#listbox.config(font=('', 12))
#listbox.pack(side='left',fill='y')
listbox.place(x=0,y=0,height=400,width=300)

scrollbar.config(command=listbox.yview)
#scrollbar.pack(side='right', fill='y')
scrollbar.place(x=300,y=0,height=400,width=20)


listbox2 = tk.Listbox(master=frame3, width=180, height= 400)
#listbox2.config(font=('', 12))
listbox2.pack()


cnt = 0

'''
for sentence in tqdm(tokenized_data):


    for word in sentence:

        if word not in adding:
            adding.append(word)
            listbox.insert(cnt, word)
            cnt = cnt + 1
            '''

vocab = model.wv.index_to_key

for word in vocab:
    word = " " + word
    listbox.insert(cnt, word)
    cnt = cnt + 1

with open('total.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(tokenized_data)
    writer.writerow(adding)


window.mainloop()

