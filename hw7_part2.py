# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 15:59:51 2022

@author: Philip Paterson
HW07 Part 2
This program finds and outpits the best and worst movies based on the 
inputted year range and the weights for IMDB ratings and twitter ratings.
"""

# Import statements
import json

# Defining the functions
def movie_data_print(movie_data, movie_type):
    '''
    This function formats the associated data for the movie: the year range,
    movie name, and combined rating.

    Parameters
    ----------
    movie_data : TUPLE
        The associated data for the movie. The first item is the combined
        rating, the second item is the movie name, and the third item is
        individual information about the movie.
    movie_type : STR
        It's either the "Best" or "Worst" movie to be printed.

    Returns
    -------
    None.

    '''
    print()
    print(movie_type.title() + ':')
    print(" " * 8 + "Released in {0}, {1} has a rating of {2:.2f}".format(
        movie_data[2]['movie_year'],
        movie_data[1],
        movie_data[0]
        ))

# Main body of the code
if __name__ == "__main__":
    # Given code
    movies = json.loads(open("movies.json").read())
    ratings = json.loads(open("ratings.json").read())
    
    # Getting the inputs
    year_min = input("Min year => ").strip()
    print(year_min)
    year_min = int(year_min)
    year_max = input("Max year => ").strip()
    print(year_max)
    year_max = int(year_max)
    w1 = input("Weight for IMDB => ").strip()
    print(w1)
    w1 = float(w1)
    w2 = input("Weight for Twitter => ").strip()
    print(w2)
    w2 = float(w2)

    # The main while loop running the program
    run = True
    while run:
        genre = input("\nWhat genre do you want to see? ").strip()
        print(genre)
        genre = genre.title()
        if genre == "stop".title():
            run = False
        else:
            # Creating a list of the data for the valid movies
            valid_movies = list()
            for movie_num in movies:
                movie_data = movies[movie_num]
                if genre in movie_data['genre']:
                    if movie_data['movie_year'] >= year_min and movie_data['movie_year'] <= year_max:
                        if movie_num in ratings:
                            movie_ratings = ratings[movie_num]
                            if len(movie_ratings) >= 3:
                                imdb_rating = movie_data['rating']
                                average_twitter_rating = sum(movie_ratings) / len(movie_ratings)
                                combined_rating = (w1 * imdb_rating + w2 * average_twitter_rating) / (w1 + w2)
                                valid_movies.append((combined_rating, movie_data['name'], movie_data))
            valid_movies.sort(reverse= True)
            
            # To execute if there are no valid movies for the genre
            if len(valid_movies) == 0:
                print("\nNo {0} movie found in {1} through {2}".format(
                    genre,
                    year_min,
                    year_max
                    ))
            else:
                # Finds and prints the best and worst movies for the associated
                # genre.
                best_movie_data = valid_movies[0]
                worst_movie_data = valid_movies[-1]
                
                movie_data_print(best_movie_data, "Best")
                movie_data_print(worst_movie_data, "Worst")