import streamlit as st
import json

#import classifier that we made using knn model classifier
from knn_classif import KnnClass
from operator import itemgetter

# Load data and movies list from corresponding JSON files


#here we will read the data from the files for processing
with open(r'data.json', 'r+', encoding='utf-8') as f:
    data = json.load(f)

#we get all the movie titles from the json file
with open(r'titles_new.json', 'r+', encoding='utf-8') as f:
    movie_titles = json.load(f)



# Here test_point is whether the user selects :
#  Movie or Genres as filter

#  k - nos of k nearest neighbors


def knn_model(test_point, k):


    # Create dummy target variable for the KNN Classifier
    target = [0 for item in movie_titles]


    # Instantiate object for the Classifier

    #here we pass in all the data so that we can classify the data
    model = KnnClass(data, target, test_point, k=k)


    # Run the algorithm
    #Train the model using data based on similarity of user query
    model.fit()


    # Distances to most distant movie
    # List will be sorted from nearest data to farthest data based on similarity
    max_dist = sorted(model.distances, key=itemgetter(0))[-1]


    # Print list of 10 recommendations < Change value of k for a different number 

    #empty table list
    table = list()

    #print all the movie list of top 10 recommendation titles
    for i in model.indices:
        # Returns back movie title and imdb link
        table.append([movie_titles[i][0], movie_titles[i][2]])

        #return full list of movie_data and titles
    return table



if __name__ == '__main__':

    #List of all genres in the dataset
    genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
              'Fantasy', 'Film-Noir', 'Game-Show', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News',
              'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Thriller', 'War', 'Western']


    #we extract the movie titles
    movies = [title[0] for title in movie_titles]

    # heading for streamlit app
    st.header('Movie Recommendation System') 

    #option for choosing our "test_point"
    #either movie or genres searches
    apps = ['Search Type', 'Movie based', 'Genres based'] 

    #this dropbox contains the list of options
    app_options = st.selectbox('Select search option:', apps)
    

    
    #If user selects Movie based then use this...
    

    if app_options == 'Movie based':

        #display all the movie list in the options 
        movie_select = st.selectbox('Select movie:', ['Avatar'] + movies)
        if movie_select == 'Pick your favourite':
            st.write('Select a movie')

        #once option selected diplay all the movie recommended list    
        else:

            #number of movies that can be displayed 
            #step ->size increment
            #max_value->max results
            n = st.number_input('Number of movies:', min_value=5, max_value=20, step=1)
            genres = data[movies.index(movie_select)]

            #place the input fromuser to test_point

            test_point = genres

            #then pass it to knn_model to find similar movies
            table = knn_model(test_point, n)

            #display the movie title and link from the table that has all this data
            for movie, link in table:
                # Displays movie title with link to imdb
                st.markdown(f"[{movie}]({link})")

    #search by gneres 
    # app[2] -> Genresbased          
    elif app_options == apps[2]:
        #display option to select genres
        options = st.multiselect('Select genres:', genres)


        #display imdb score slider
        if options:

            #min_val -1 
            #max_val-10
            #default recommendation - 8 rating
            imdb_score = st.slider('IMDb score:', 1, 10, 8)


            #number of recommendations we get 
            n = st.number_input('Number of movies:', min_value=5, max_value=20, step=1)

            #if 
            test_point = [1 if genre in options else 0 for genre in genres]

            #get all the imdb scores and append it to test_points
            test_point.append(imdb_score)

            #pass the scores to knn_model
            #to find nearest results to these ratings
            table = knn_model(test_point, n)

            #display the results
            for movie, link in table:
                # Displays movie title with link to imdb
                st.markdown(f"[{movie}]({link})")

        #
        else:
                st.write("We couldn't find anything similar to waht you asked for :/ "
                        "You can select the genres and change the IMDb score.")

    else:
        st.write('Select option')