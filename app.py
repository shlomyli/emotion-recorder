import streamlit as st
import time
import pandas as pd
import base64


def start_video():
    st.session_state.start_time = time.time()
    st.session_state.playing = True


def record_rating():
    elapsed = time.time() - st.session_state.start_time
    current = st.session_state.rating_slider

    if st.session_state.last_rating is None or current != st.session_state.last_rating:
        st.session_state.ratings.append((elapsed, current))
        st.session_state.last_rating = current


def start_edit():
    st.session_state.edit_mode = True
    st.session_state.editable_df = st.session_state.df_ratings.copy()


st.image(
    "https://media.licdn.com/dms/image/v2/D4D0BAQEL_RCJAemS_w/company-logo_200_200/company-logo_200_200/0/1726498371243/brainvivo_logo?e=1744848000&v=beta&t=XiSuWtr_S4LdYCnTF_AoZRKlx6FBIQ94sjDiL39rGnE",
    width=100,
    caption="",
)

st.title("Emotion Rating")

uploaded_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi"])
if uploaded_file:
    # Reset state whenever a new file is uploaded
    if (
        "current_file" not in st.session_state
        or st.session_state.current_file != uploaded_file.name
    ):
        st.session_state.current_file = uploaded_file.name
        st.session_state.start_time = None
        st.session_state.playing = False
        st.session_state.ratings = []
        st.session_state.last_rating = None
        st.session_state.show_editor = False
        st.session_state.df_ratings = None
        st.session_state.edit_mode = False
        st.session_state.editable_df = None

    # Display the video
    st.video(uploaded_file)

    # Show “Start Video” button until clicked
    if not st.session_state.playing:
        st.button("▶️ Press whenever the video starts playing", on_click=start_video)

    # Once clicked, render video with autoplay via HTML
    if st.session_state.playing:
        # Slider for rating
        st.slider(
            "Emotion rating (0–7)",
            0.0,
            7.0,
            3.5,
            0.1,
            key="rating_slider",
            on_change=record_rating,
        )

        # Show & download ratings
        if st.session_state.ratings:
            st.session_state.df_ratings = pd.DataFrame(
                st.session_state.ratings, columns=["timestamp (s)", "rating"]
            )
            st.write("### Recorded Ratings")
            st.dataframe(st.session_state.df_ratings)
            st.button("Edit/Download", on_click=start_edit)

        if st.session_state.edit_mode:
            edited = st.data_editor(
                st.session_state.editable_df,
                use_container_width=True,
                num_rows="dynamic",
            )

            # Download the edited table
            csv = edited.to_csv(index=False).encode("utf-8")
            filename = uploaded_file.name.rsplit(".", 1)[0] + "_ratings.csv"
            st.download_button(
                "Download CSV", data=csv, file_name=filename, mime="text/csv"
            )
