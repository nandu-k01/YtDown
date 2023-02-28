import streamlit as st
from pytube import YouTube
import base64


st.title("Youtube Video Downloader") 
st.subheader("Enter the URL:")
url = st.text_input(label='URL')

if url != '':
    yt = YouTube(url)
    st.image(yt.thumbnail_url, width=300)
    st.subheader('''
    {}
    ## Length: {} seconds
    ## Rating: {} 
    '''.format(yt.title , yt.length , yt.rating))
    video = yt.streams
    if len(video) > 0:
        downloaded , download_audio = False , False
        download_video = st.button("Video")
        if yt.streams.filter(only_audio=True):
            download_audio = st.button("Audio Only")
        if download_video:
            video_path = video.get_highest_resolution().download()
            downloaded = True
        if download_audio:
            video_path = video.filter(only_audio=True).first().download()
            downloaded = True
        if downloaded:
            with open(video_path, 'rb') as f:
                video_bytes = f.read()
            b64_video = base64.b64encode(video_bytes).decode()
            st.markdown(f'<button href="data:video/mp4;base64,{b64_video}" download="{yt.title}.mp4" class= "download-button">Save to system</button>', unsafe_allow_html=True)
            st.markdown(
                """
<style>
        .download-button {
            background-color: rgb(19, 23, 32);
            color: white;
            padding: 8px 16px;
            border-color: rgba(62, 53, 53, 0.592);
            border-radius: 5px;
            border-width: 2px;
            text-decoration: none;
            font-size: 16px;
            margin-top: 16px;
        }
    
        .download-button:hover {
            background-color: rgb(19, 23, 32);
            color: rgb(212, 64, 64);
            border-color: rgb(212, 64, 64);

        }
    </style>
                """,
                unsafe_allow_html=True
            )           
            st.subheader("Download Complete")
    else:
        st.subheader("Sorry, this video can not be downloaded")