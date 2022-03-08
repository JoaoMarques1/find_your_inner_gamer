from urllib import response
import streamlit as st
import requests
from find_your_inner_gamer.gcp import get_data_from_gcp
import streamlit as st
from find_your_inner_gamer.utils import get_img

#API url
url = 'https://find-your-inner-gamer-7oqykbx6lq-ew.a.run.app/predict'

# configuring page with wide view
st.set_page_config(
    page_title="Find Your Inner Gamer!",
    page_icon="🕹️", layout="wide"
)

# setting default value for clik variable to False
clik = False

# Creating three columns and putting title in the middle
c30, c31, c32 = st.columns([5, 10, 5])
with c31:
    st.title("🎮 Find Your Inner Gamer")
    st.header("")


st.image('https://images.newscientist.com/wp-content/uploads/2021/10/27162905/PRI_207080436.jpg?crop=16:9,smart&width=1200&height=675&upscale=true')
# Creating the about this app
with st.sidebar:
    with st.expander("ℹ️ - About this app", expanded=True):
        st.write(
        """
    🦁 Created with Love in Le Wagon by Luis Quieros, Joao Marques, Laura Bonnet 🦁
	    """
    )
    st.markdown("")
    st.markdown("")


# Creating the drop down for user to choose the game
    @st.cache
    def get_select_box_data():
        return get_data_from_gcp()
    df = get_select_box_data()

    game = st.selectbox('Select your favourite game', df['name'], help="At present, you can choose between 24 000 games. More to come!")
    params = {
            'game': game
        }
    st.markdown('')

    cs, c1, c2 = st.columns([1, 6, 1])
    with c1:
        if st.button('✨ Find Similar Games'):
            response = requests.get(url, params)
            pred = response.json()
            clik = True


# creating font
st.markdown("""
<style>
.small-font {
    font-size:10px !tags;
}
</style>
""", unsafe_allow_html=True)


# displaying recommended titles
if clik :

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    cols = [st.columns(2) for n in range(len(pred['title']))]

    for game, col in zip (pred['title'][1:5] , [col1,col2,col3,col4]):

        row = df[df['name']== game]

        col.header(f"{game}")
        col.markdown(f"<p class='small-font'>{' '.join(row['tags'])}</p>", unsafe_allow_html=True)
        col.image(get_img(row['url'].iloc[0]),

                    use_column_width=True, # Manually Adjust the width of the image as per requirement
                )
        col.write(f"{' '.join(row['game_description'])}", use_column_width=True)
        col.write(f"{row['url'].iloc[0]}", use_column_width=True)
        col.write(f"{row['reviews'].iloc[0]}", use_column_width=True)
