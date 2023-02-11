import streamlit as st
import youtube_dlc
import moviepy.editor as mp
import os


def download_video(url, name):
    ydl_opts = {
        'outtmpl': f'{name}.%(ext)s',
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
    }
    with youtube_dlc.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def convert_to_audio(video_file, audio_file):
    clip = mp.VideoFileClip(video_file)
    clip.audio.write_audiofile(audio_file)

def cut_audio(audio_file, cut_file, sec):
    clip = mp.AudioFileClip(audio_file)
    clip_cut = clip.subclip(0, sec)
    clip_cut.write_audiofile(cut_file)

def merge_audios(files, output_file):
    clips = [mp.AudioFileClip(f) for f in files]
    concat_clip = mp.concatenate_audioclips(clips)
    concat_clip.write_audiofile(output_file)

def main():
    st.markdown("<h2 style='text-align: center; color: white;'>Mash-up </h2>", unsafe_allow_html=True)
    #st.title("MASHUP")
    from PIL import Image
    image = Image.open('image4.jpg')
    base="dark"
    primaryColor="purple"
    st.image(image, caption='Music')
    N = st.number_input("Enter the number of videos to download", value=1, min_value=1)
    X = st.text_input("Enter the singer name", value='.')
    Y = st.number_input("Enter the number of seconds to cut from each video", value=20, min_value=20)
    
    if st.button("Download and Merge"):
        st.success("Files merged successfully.....Check your location folder")
        try:
            # Download the videos
            video_files = []
            for i in range(N):
                url = f"https://www.youtube.com/results?search_query={X}+song+{i}"
                download_video(url, f"video_{i}")
                video_files.append(f"video_{i}.mp4")

            
            # Convert videos to audio
            audio_files = []
            for v in video_files:
                a = v.replace('.mp4', '.wav')
                convert_to_audio(v, a)
                audio_files.append(a)
            
            # Cut audio files
            cut_files = []
            for a in audio_files:
                c = a.replace('.wav', '_cut.wav')
                cut_audio(a, c, Y)
                cut_files.append(c)
            
            # Merge audio files
            merge_audios(cut_files, "output.wav")
            st.success("Files merged successfully")
            save_location = st.text_input("Enter the save location to save the audio file:", value=".")
            merge_audios.write_audiofile(os.path.join(save_location, "output.wav"))
        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == '__main__':
    main()