from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time


subscription_key = "02427c5fc13241389bf8e0c91fd11a76"
endpoint = "https://udemy-20210522.cognitiveservices.azure.com/"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))


def get_tags(filepath):
    local_image = open(filepath, "rb")

    tags_result = computervision_client.tag_image_in_stream(local_image )
    tags = tags_result.tags
    tags_name = []
    for tag in tags:
        tags_name.append(tag.name)
    return tags_name


def get_adult(filepath):
    local_image = open(filepath, "rb")

    image_features = ["adult"]
    detect_adult_results = computervision_client.analyze_image_in_stream(local_image, image_features)
    score = detect_adult_results.adult.adult_score * 100
    return score



def detect_objects(filepath):
    local_image = open(filepath, "rb")

    detect_objects_results = computervision_client.detect_objects_in_stream(local_image)
    objects = detect_objects_results.objects
    return objects


import streamlit as st
from PIL import ImageDraw
from PIL import ImageFont

st.title('エッチ度確認アプリ')

uploaded_file = st.file_uploader('Choose an image...', type=['jpg', 'png'])
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    img_path = f'img/{uploaded_file.name}'
    img.save(img_path)
    objects = detect_objects(img_path)


    #描画
    draw = ImageDraw.Draw(img)
    for object in objects:
        x = object.rectangle.x
        y = object.rectangle.y
        w = object.rectangle.w
        h = object.rectangle.h
        caption = object.object_property

        font = ImageFont.truetype(font='./Helvetica 400.ttf', size=50)
        text_w, text_h = draw.textsize(caption, font=font)

        draw.rectangle([(x, y), (x+w, y+h)], fill=None, outline='green', width=7)
        draw.rectangle([(x, y), (x+text_w, y+text_h)], fill='green', width=7)
        draw.text((x, y), caption, fill='white', font=font)

    st.image(img)

    tags_name = get_tags(img_path)
    tags_name = ', '.join(tags_name)

    adult_score = get_adult(img_path)

    st.markdown('**認識されたコンテンツタグ**')
    st.markdown(f'> {tags_name}')
    st.markdown('**エッチ度測定結果**')
    if adult_score > 80:
        st.markdown(f'> エッチ度{adult_score:.2f}%だ！エッチコンロ点火！ｴﾁﾁﾁﾁﾁﾁﾁﾁﾁｗ')
    elif adult_score > 50:
        st.markdown(f'> {adult_score:.2f}%のエロさです。まあまあエロいです。')
    elif adult_score > 30:
        st.markdown(f'> {adult_score:.2f}%のエロさです。ちょっとのエロさ。')
    else:
        st.markdown(f'> {adult_score:.2f}%のエロさです。健全な画像です。')