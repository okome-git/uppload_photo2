import streamlit as st
from PIL import Image
import boto3
import os
import time

st.set_page_config(
    page_title = 'Photo Upload',
    page_icon = '๐ท',
)

pre_password = st.secrets["PRE_PASSWORD"]
input_password = st.text_input("ใในใฏใผใ", help="ไบๅใซไบๅๅฑใใ้็ฅใใใใในใฏใผใใๅ่ง่ฑๆฐๅญใงๅฅๅใใฆใใ ใใ", value="", type="password")

if str(pre_password) != str(input_password):
    st.warning('ๅ็ใๆ็จฟใใใซใฏใในใฏใผใใๅฅๅใใฆใใ ใใ')
    st.stop()
    
tempo = st.success('่ช่จผๆๅ')
time.sleep(1)
tempo.balloons()

s3 = boto3.client('s3',
        aws_access_key_id= st.secrets["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key= st.secrets["AWS_SECRET_ACCESS_KEY"] ,
        region_name='ap-northeast-1'
)

st.write(
    """
    # ๆ้ใปPFC ใใฉใใณใณใในใ ๏ผ๏ผ๏ผ๏ผ
    ## ๅ็ใขใใใญใผใใทในใใ 
    ### ๅ็ใจใณใกใณใใๅฅๅใใฆใใ ใใ
    """
)

with st.form(key='my_form'):
    st.write("็ปๅใใกใคใซใใขใใใญใผใใใฆใใ ใใใ๏ผpngใjpegใjpgๅฝขๅผใฎใฟๅฏพๅฟใใฆใใพใใ๏ผ")
    uploaded_file =  st.file_uploader("ใใกใคใซใขใใใญใผใ", type=['png','jpeg','jpg'])
    sales_id = st.text_input(label='็คพๅก็ชๅทใๅ่งใงๅฅๅใใฆใใ ใใ')
    department = st.selectbox("้จ็ฝฒใ้ธใใงใใ ใใใ",("่จๆธฌๅถๅพก","IA3"))
    nick_name = st.text_input(label='ใใใฏใใผใ ใๅฅๅใใฆใใ ใใ๏ผไปปๆ๏ผ')
    img_type = st.selectbox("ๆๅบๅใฎ้จ้ใ้ธๆใใฆใใ ใใ",("้ขจๆฏ","็ใ็ฉ","AIใ้้ใใใ","ในใใคใใผใ ","่ฒทใฃใฆใใใฃใใใฎ","ๆ ใ"))
    img_title = st.text_input('ๅ็ใฎใฟใคใใซใๅฅๅใใฆใใ ใใ')
    comment = st.text_area('ๅ็ใซๅฏพใใใณใกใณใใๅฅๅใใฆใใ ใใ')
    submit_button = st.form_submit_button(label='ๆๅบ')

if uploaded_file is not None:
    #file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
    #st.write(file_details)
    # st.write(uploaded_file)
    try:
        img = Image.open(uploaded_file)
        name = uploaded_file.name
        st.image(img, caption=name)
    except:
        st.error("ใใฎใใกใคใซใฏ็ปๅใงใฏใชใใฎใงใใฌใใฅใผใงใใพใใ")


if submit_button == True:
    try:
        os.makedirs("./uploaded/", exist_ok=True)
        img.save("./uploaded/" + name )
        st.write(comment)
        s3 = boto3.resource('s3') #S3ใชใใธใงใฏใใๅๅพ
        bucket = s3.Bucket('photocontest')
        bucket.upload_file("./uploaded/" + name, name)
        os.remove("./uploaded/" + name)

    except:
        st.error("ใใฎใใกใคใซๅฝขๅผใฏๅฏพๅฟใใฆใใพใใใ'png','jpeg','jpg'ๅฝขๅผใงๅๅบฆใขใใใญใผใใใฆใใ ใใใ")
