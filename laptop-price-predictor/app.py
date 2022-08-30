import pickle
import numpy as np
import streamlit as st
from babel.numbers import format_currency
import urllib.request

# import the model
# pipe = pickle.load(open('pipe.pkl','rb'))
# df = pickle.load(open('df.pkl','rb'))


# pipe = pickle.load(urllib.request.urlopen(("https://drive.google.com/uc?export=download&id=1flf5wheLXQYos-5Nuy9PPGn79cDNppFM")))
# df = pickle.load(urllib.request.urlopen(("https://drive.google.com/uc?export=download&id=14-zRh0M2sCNCf4wF_IazLEvrgSyb_YsP")))

url1 = "https://www.googleapis.com/drive/v3/files/1flf5wheLXQYos-5Nuy9PPGn79cDNppFM?alt=media&key=AIzaSyCUpIPtvM6lJw65WnZoM-Xxn7Xo6xytJ3k"
url2 = "https://www.googleapis.com/drive/v3/files/14-zRh0M2sCNCf4wF_IazLEvrgSyb_YsP?alt=media&key=AIzaSyCUpIPtvM6lJw65WnZoM-Xxn7Xo6xytJ3k"
pipe = pickle.load(urllib.request.urlopen(url1))
df = pickle.load(urllib.request.urlopen(url2))

st.title("Laptop Price Predictor")

# brand
company = st.selectbox('Brand',df['Company'].unique())

# type of laptop
type = st.selectbox('Type',df['TypeName'].unique())

# Ram
ram = st.selectbox('RAM(in GB)',[2,4,6,8,12,16,24,32,64])

# weight
weight = st.selectbox('Weight(in KG)',[0.4 , 0.6 , 0.8 , 1.0 , 1.2 , 1.4 , 1.6 , 1.8 , 2.0 , 2.2 , 2.4 , 2.6 , 2.8 , 3.0 , 3.2 , 3.4 , 3.6 , 3.8 , 4.0  ])

# Touchscreen
touchscreen = st.selectbox('Touchscreen',['No','Yes'])

# IPS
ips = st.selectbox('IPS',['No','Yes'])

# screen size
screen_size = st.selectbox('Screen Size(in inches)',[12.0 , 12.5 , 13.0 , 13.5 , 14.0 , 14.5 , 15.0 , 15.5 , 16.0 , 16.5 , 17.0 , 17.5 ])

# resolution
resolution = st.selectbox('Screen Resolution',sorted(['1920x1080','1366x768','1600x900','3840x2160','3200x1800','2880x1800','2560x1600','2560x1440','2304x1440']))

#cpu
cpu = st.selectbox('CPU',df['Cpu brand'].unique())


hdd = st.selectbox('HDD(in GB)',sorted(df['HDD'].unique()))

ssd = st.selectbox('SSD(in GB)',sorted(df['SSD'].unique()))

gpu = st.selectbox('GPU',df['Gpu brand'].unique())

os = st.selectbox('OS',df['os'].unique())

try:
    if st.button('Predict Price'):

        if touchscreen == 'Yes':
            touchscreen = 1
        else:
            touchscreen = 0

        if ips == 'Yes':
            ips = 1
        else:
            ips = 0

        # resolution = 1920x1080 after split by x is [1920,1080]
        X_res = int(resolution.split('x')[0]) # 1920
        Y_res = int(resolution.split('x')[1]) # 1080
        ppi = ((X_res**2) + (Y_res**2))**0.5/screen_size    # ((1920**2) + (1080**2))**0.5/15.6 = 141.21
        query = np.array([company,type,ram,weight,touchscreen,ips,ppi,cpu,hdd,ssd,gpu,os])

        query = query.reshape(1,12)
        finalprice = int(np.exp(pipe.predict(query)[0]))
        finalprice = format_currency(finalprice, 'INR', locale='en_IN')
        # st.title("The predicted price of this configuration is " +str(finalprice)) 
        st.markdown(f"<p style='font-size: 30px;'>The predicted price of your configuration is  <b style='color: green;'>{finalprice}</b></p>", unsafe_allow_html=True)
except:
    st.markdown(f"<strong style='font-size: 45px;color: red;'>Opps!! Something is wrong please check and try again </strong>", unsafe_allow_html=True)
