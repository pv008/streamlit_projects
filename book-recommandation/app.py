import streamlit as st 
import pickle
import pandas as pd 
import numpy as np
import urllib.request

# model = pickle.load(open('modelpkl.pkl','rb'))
# book_pivot = pickle.load(open('book_pivotpkl.pkl','rb'))
# final_img_url = pd.read_csv('final_img_url.csv')

model = pickle.load(urllib.request.urlopen('https://drive.google.com/uc?export=download&id=1oE7rVB8Kw9Q1dT9aiLJ0ERiKt7WqSZ77'))
book_pivot = pickle.load(urllib.request.urlopen('https://drive.google.com/uc?export=download&id=1x7g-uMesHi-YwRINjhGkOgcEhhlK3W5-'))
final_img_url = pd.read_csv('final_img_url.csv')

st.title('Book Recommandation')

selected_book = st.selectbox('Select Book',sorted(final_img_url['title'].values))

def recommand_book1(book_name):
    book_id = np.where(book_pivot.index == book_name)[0][0]
    distances, suggestions = model.kneighbors(book_pivot.iloc[book_id, :].values.reshape(1,-1),n_neighbors=6)
    book_recommnd = []
    for i in suggestions[0]: # coz its 2d array [[like]]
#         if suggestions[0][0] != i:   # we don't want print 1st book coz it itself
        book_recommnd.append(book_pivot.index[i])
#     return book_recommnd
    
    book_name = []
    book_link = []
    for bookname in book_recommnd:
        if bookname != book_recommnd[0]: # we don't want print 1st book coz it itself
            book_name.append(bookname)
            book_link.append(final_img_url[final_img_url['title'] == bookname]['url'].values[0])

    return book_name,book_link

if st.button('Recommand'):
    book,link = recommand_book1(selected_book)

    col1,col2,col3,col4,col5 = st.columns(5)

    with col1:
        st.text(book[0])
        st.image(link[0])
    with col2:
        st.text(book[1])
        st.image(link[1])
    with col3:
        st.text(book[2])
        st.image(link[2])
    with col4:
        st.text(book[3])
        st.image(link[3])
    with col5:
        st.text(book[4])
        st.image(link[4])