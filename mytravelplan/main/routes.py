from flask import render_template, request, Blueprint
from flask_login import login_required, current_user
from sqlalchemy import desc
from mytravelplan import db
from mytravelplan.messages.routes import messages_counters
from mytravelplan.models import Post, User, PostLikes, Country
from mytravelplan.posts.forms import SearchForm, LikeForm, ReportForm

main = Blueprint('main', __name__)


# Func like & unlike post
def like_to_post(id_of_post_to_like, like_or_unlike):
    if PostLikes.query.filter_by(post_id=id_of_post_to_like,
                                 username=current_user.username).first() == None and like_or_unlike == 'like':
        post_likes = PostLikes(post_id=id_of_post_to_like, username=current_user.username)
        db.session.add(post_likes)
        post = Post.query.filter_by(id=id_of_post_to_like).first()
        post.amount_of_likes += 1
        db.session.commit()
    elif PostLikes.query.filter_by(post_id=id_of_post_to_like,
                                   username=current_user.username).first() != None and like_or_unlike == 'unlike':
        post = Post.query.filter_by(id=id_of_post_to_like).first()
        post.amount_of_likes -= 1
        post_likes = PostLikes.query.filter_by(post_id=id_of_post_to_like, username=current_user.username).first()
        db.session.delete(post_likes)
        db.session.commit()
    return


# Main func show the main page with all posts with of all users
@main.route('/', methods=['GET', 'POST'])
@main.route('/home', methods=['GET', 'POST'])
def home():
    form = LikeForm()
    reported_form = ReportForm()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(find_friends=False).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    # If like or unlike button were clicked
    if current_user.is_authenticated:
        if form.validate_on_submit():
            like_or_unlike = form.like_or_unlike.data
            id_of_post_to_like = form.id.data
            like_to_post(id_of_post_to_like, like_or_unlike)
        # If report post was clicked
        if reported_form.validate_on_submit():
            id_of_reported_post = form.id.data
            post = Post.query.get(id_of_reported_post)
            post.reported = True
            db.session.commit()

    # Generic functionality
    # Messages counters
    msg_counters = messages_counters()
    return render_template('home.html', posts=posts, form=form, reported_form=reported_form, msg_counters=msg_counters)


# Posts to find firends to travel with
@main.route('/friends', methods=['GET', 'POST'])
def find_friends():
    form = LikeForm()
    reported_form = ReportForm()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(find_friends=True).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    # If like or unlike button were clicked
    if current_user.is_authenticated:
        if form.validate_on_submit():
            like_or_unlike = form.like_or_unlike.data
            id_of_post_to_like = form.id.data
            like_to_post(id_of_post_to_like, like_or_unlike)
        # If report post was clicked
        if reported_form.validate_on_submit():
            id_of_reported_post = form.id.data
            post = Post.query.get(id_of_reported_post)
            post.reported = True
            db.session.commit()

    # Generic functionality
    # Messages counters
    msg_counters = messages_counters()
    return render_template('home.html', posts=posts, form=form, reported_form=reported_form, msg_counters=msg_counters)


# Func shows most liked posts
@main.route('/mostlikedposts', methods=['GET', 'POST'])
def most_liked_posts():
    form = LikeForm()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.amount_of_likes.desc()).paginate(page=page, per_page=5)
    # If like or unlike button were pressed
    if form.validate_on_submit():
        like_or_unlike = form.like_or_unlike.data
        id_of_post_to_like = form.id.data
        like_to_post(id_of_post_to_like, like_or_unlike)

    # Generic functionality
    # Messages counters
    msg_counters = messages_counters()
    return render_template('most_liked_posts.html', posts=posts, form=form, msg_counters=msg_counters)


# Most visited countries graph show
@main.route('/countries')
def most_visited_countries():
    most_visited_countries = Country.query.order_by(desc(Country.visit_count)).limit(5).all()
    most_visited_countries_dictionary = {}
    i = 0
    for country in most_visited_countries:
        most_visited_countries_dictionary[str(i)] = countryToJSONVisited(country)
        i += 1
    print(most_visited_countries_dictionary.values())

    # Generic functionality
    # Messages counters
    msg_counters = messages_counters()
    return render_template('most_visited_countries.html', json_countries=most_visited_countries_dictionary,
                           msg_counters=msg_counters)


# Most rated countries graph show
@main.route('/rated')
def most_rated_countries():
    most_rated_countries = Country.query.order_by(desc(Country.rate_avg)).limit(5).all()
    most_rated_countries_dictionary = {}
    i = 0
    for country in most_rated_countries:
        print(country.rate_avg)
        most_rated_countries_dictionary[str(i)] = countryToJSONRated(country)
        i += 1
    print(most_rated_countries_dictionary.values())

    # Generic functionality

    # Messages counters
    msg_counters = messages_counters()

    return render_template('most_rated_countries.html', json_countries=most_rated_countries_dictionary,
                           msg_counters=msg_counters)


# Transforming object in python format to json format with visits var
def countryToJSONVisited(country):
    return {'name': country.country_name,
            'visits': country.visit_count}


# Transforming object in python format to json format with rated var
def countryToJSONRated(country):
    return {'name': country.country_name,
            'rate': country.rate_avg}


# About func show the about page
@main.route('/about')
def about():
    # Generic functionality
    # Messages counters
    msg_counters = messages_counters()
    return render_template('about.html', title='About', msg_counters=msg_counters)


# Search func
@main.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    posts = []
    posts_results = set()


    if form.validate_on_submit():
        if form.country.data != '':
            country_name = form.country.data.lower()
            country_name = country_name.capitalize()
            posts_country = Post.query.filter_by(country=country_name)
            posts.extend(posts_country)

        if form.city.data != '':
            city_name = form.city.data.lower()
            city_name = city_name.capitalize()
            posts_city = Post.query.filter_by(city=city_name)
            posts.extend(posts_city)

        if form.place.data != '':
            place_name = form.place.data.lower()
            place_name = place_name.capitalize()
            posts_place = Post.query.filter_by(place=place_name)
            posts.extend(posts_place)

        posts_results = set(posts)


        msg_counters = messages_counters()
        return render_template('searched_posts.html', posts=posts_results, msg_counters=msg_counters)
    # Generic functionality
    # Messages counters
    msg_counters = messages_counters()
    return render_template('search.html', form=form, msg_counters=msg_counters)
