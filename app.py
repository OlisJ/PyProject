import streamlit as st
import database
from models import Game, GameCreate


st.title("Pixel Archive")
st.write("Discover and explore a curated collection of video games!")
st.write("Run by the community for the community.")
def main():
    st.subheader("Game Search")
    
    with st.sidebar.form("search_form"):
        st.write("Search Games")
        
        name = st.text_input("Game Name")
        genre = st.text_input("Genre")
        
        col1, col2 = st.columns(2)
        with col1:
            min_price = st.number_input("Min Price", min_value=0.0, value=0.0)
        with col2:
            max_price = st.number_input("Max Price", min_value=0.0, value=1000.0)
            
        release_date = st.text_input("Release Date (YYYY)")
        

        search_button = st.form_submit_button("Search")
        
        if search_button:
            games = database.search_games(
                name=name if name else None,
                genre=genre if genre else None,
                min_price=min_price if min_price > 0 else None,
                max_price=max_price if max_price < 1000 else None,
                release_date=release_date if release_date else None
            )
            
            st.session_state.search_results = games
    
    if 'search_results' in st.session_state:
        st.write(f"Found {len(st.session_state.search_results)} games:")
        
        for game in st.session_state.search_results:
            with st.expander(f"{game.name} - {game.genre}"):
                st.write(f"**Description:** {game.description}")
                st.write(f"**Price:** ${game.price:.2f}")
                st.write(f"**Release Date:** {game.release_date}")
    else:
        st.write("Use the search form on the left to find games!")

    # Add game form in the right sidebar
    with st.sidebar:
        st.markdown("---")  # Add a separator between search and add forms
        st.subheader("Add New Game")
        with st.form("add_game_form"):
            new_name = st.text_input("Game Name*")
            new_description = st.text_area("Description*")
            new_price = st.number_input("Price*", min_value=0.0, value=0.0, step=0.01)
            new_genre = st.text_input("Genre*")
            new_release_date = st.text_input("Release Date* (YYYY-MM-DD)")
            
            submit_button = st.form_submit_button("Add Game")
            
            if submit_button:
                if new_name and new_description and new_genre and new_release_date:
                    try:
                        new_game = GameCreate(
                            name=new_name,
                            description=new_description,
                            price=new_price,
                            genre=new_genre,
                            release_date=new_release_date
                        )
                        game_id = database.create_game(new_game)
                        st.success(f"Successfully added {new_name} to the database!")
                        
                        # Clear the search results to show updated data
                        if 'search_results' in st.session_state:
                            del st.session_state.search_results
                            st.experimental_rerun()
                    except Exception as e:
                        st.error(f"Error adding game: {str(e)}")
                else:
                    st.error("Please fill out all required fields marked with *")

if __name__ == "__main__":
    main()