import streamlit as st
from PIL import Image
import numpy as np
import boto3
import s3fs
import os

st.set_page_config(
    page_title = 'Photo Upload',
    page_icon = '📷',
)

# st.write(st.secrets["AWS_ACCESS_KEY_ID"])
# st.write(st.secrets["AWS_SECRET_ACCESS_KEY"])
# fs = s3fs.S3FileSystem(anon=False)

s3 = boto3.client('s3',
        aws_access_key_id= st.secrets["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key= st.secrets["AWS_SECRET_ACCESS_KEY"] ,
        region_name='ap-northeast-1'
)

st.write(
    """
    # 技開・PFC フォトコンテスト ２０２１
    ## 写真アップロードシステム
    ### 写真とコメントを入力してください
    """
)

with st.form(key='my_form'):
    st.write("画像ファイルをアップロードしてください。（png、jpeg、jpg形式のみ対応しています。）")
    uploaded_file =  st.file_uploader("ファイルアップロード", type=['png','jpeg','jpg'])
    sales_id = st.text_input(label='社員番号を半角で入力してください')    
    comment = st.text_input('写真に対するコメントを入力してください')
    submit_button = st.form_submit_button(label='提出')

if uploaded_file is not None:
    #file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
    #st.write(file_details)
    # st.write(uploaded_file)
    try:
        img = Image.open(uploaded_file)
        name = uploaded_file.name
        st.image(img, caption=name)
    except:
        st.error("このファイルは画像ではないのでプレビューできません")


if submit_button == True:
    try:
        os.makedirs("./uploaded/", exist_ok=True)
        img.save("./uploaded/" + name )
        st.write(comment)
        s3 = boto3.resource('s3') #S3オブジェクトを取得
        bucket = s3.Bucket('tatemizo')
        bucket.upload_file("./uploaded/" + name, name)
        os.remove("./uploaded/" + name)

    except:
        st.error("このファイル形式は対応していません。'png','jpeg','jpg'形式で再度アップロードしてください。")