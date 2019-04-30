import imdb
import random 

# ia = imdb.IMDb()

# keyword_list = ia.get_keyword('funny') # will get similar keywords to search with
# print(keyword_list)
# movie_list = ia.get_keyword('lego') # will return movies with this keyword
# # print(movie_list)
# search = movie_list[0].movieID
# print(search)
# movie = ia.get_movie(search)
# print(movie)
# print(movie.get('genre'))
# flag = 0
# genre_list = movie.get('genre')
# for elem in genre_list:
#     if elem == genre: # movie meets genre requirement
#         flag = 1


# print(search['genre'])
# call below not working
# movie = ia.search_movie(search)
# print(movie)
# jaws = ia.get_movie('0304000')
# maybe = ia.Movie.'genre'
# print(keywordList)
# print()
# print(movie_list)
# something = ia.get_movie_infoset()
# print(something)
# print(jaws)
# print(jaws.'title'())

# will take an input genre and generate 5 possible movies of interest
def movie_rec(input,sent,old):
    recs = []
    options = {
        'Action': ['destructive','violent','explosion','fast-paced','car-chase','femme-fatale','biker','heist','superhero','kung-fu'],
        'Thriller': ['dark','twisted','exciting','scary','conspiracy','psychopath','slasher','serial-killer','murder','betrayal'],
        'Comedy': ['hilarious','funny','parody','satire','black-comedy','spoof','mockumentary','joke','comedian','absurd-humor','social-satire'],
        'Animation': ['fun','delightful','cartoon','anime','based-on-comic','based-on-manga','2d-animation','stop-motion','computer-animation','cartoon'],
        'Adventure': ['explore','hazard','exciting','wild','fast-paced','epic','coming-of-age','sword','kidnapping','escape'],
        'Family': ['kids','cartoon','Disney','wholesome','family-relationships','singing','high-school','magic','talking-animal','horse'],
        'Musical': ['opera','singing','dancing','singer','song','love','montage','dance','singer','dancing'],
        'Horror': ['murder','blood','death','gore','demon','ghost','zombie','violence','knife','blood-splatter'],
        'Romance': ['singing','love','teenager','young-adults','elderly-people','kiss','male-female-relationship','dancing','bare-chested-male','love'],
        'Biography': ['character-name-in-title','independent-film','based-on-true-story','f-rated','death','singer','murder','world-war-two','politics','reenactment'],
        'Sci-Fi': ['alien','explosion','outer-space','murder','robot','monster','superhero','spaceship','surrealism','future'],
        'Drama':['based-on-novel','independent-film','murder','teenager','character-name-in-title','elderly-people','young-adults','death','cigarette-smoking','family-relationships'],
        'Mystery':['murder','flashback','based-on-novel','death','independent-film','blood','investigation','detective','bare-chested-male','kidnapping'],
        'Fantasy':['magic','character-name-in-title','surrealism','independent-film','based-on-novel','monster','fight','friendship','transformation','sword-and-sorcery'],
        'Documentary':['f-rated','character-name-in-title','independent-film','world-war-two','making-of','wildlife','food','rock-music','racism','water']

    }
    short_list = options.get(input)
    keyword = short_list[sent]
    db = imdb.IMDb()
    movie_list = db.get_keyword(keyword)
    i = 0
    j = 0
    flag = 0
    # currently not working for keywords that return an empty search
    while i < 5:
        if j == len(movie_list):
            int = random.randint(0,len(short_list)-1)
            keyword = short_list[int]
            movie_list = db.get_keyword(keyword)
            j = 0
        searchID = movie_list[j].movieID
        movie = db.get_movie(searchID)
        genre_list = movie.get('genre')
        if (movie.get('title') not in old):
            for elem in genre_list:
                if elem == input:
                    flag = 1
            if flag == 1:
                recs.append(movie.get('title'))
                i += 1
                flag = 0
        j += 1
    return recs

# will turn a sentiment input into a genre recommendation
def genre_rec(sentiment):
    # dictionary containing genres from IMDb
    options = {
        'anger': ['Action','Thriller','Adventure'],
        'fear': ['Horror','Thriller'],
        'joy': ['Comedy','Musical','Animation',],
        'sadness': ['Romance','Comedy'],
        'analytical': ['Biography','Sci-Fi','Fantasy','Documentary'],
        'confident': ['Drama','Mystery'],
        'tentative': ['Family','Romance'],
    }
    # selects a genre at random from list
    short_list = options.get(sentiment)
    int = random.randint(0,len(short_list)-1)
    return short_list[int]

def id_rec(sent):
    db = imdb.IMDb()
    movie = db.get_movie(sent)
    ret = movie.get('title')
    return ret


if __name__ == '__main__':
    # print(genre_rec('anger'))
    print(movie_rec('Comedy'))
