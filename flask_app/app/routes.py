import psycopg2
from flask import render_template, request, redirect, url_for
from .queries import queries
from datetime import datetime
from dateutil.relativedelta import relativedelta
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import uuid

from app import app
from app.forms import LoginForm, SignupForm, PostQuestionForm, ChangePasswordForm, SearchForm, EditProfileForm, EditQuestionForm, EditAnswerForm, AdminLoginForm
from app.models import User
from app import login

print("Starting routes.py")
def get_db_connection():
    conn = psycopg2.connect(
        host="10.17.50.91",
        database="group_9",
        user="group_9",
        password="6xKbIOpdFFobZr"
    )
    return conn

print("Connecting to database....")

conn = get_db_connection()
cursor = conn.cursor()

print("Connected to database successfully :)")

@login.user_loader
def load_user(id):
    cursor.execute(queries["profile"], (int(id), ))
    user = cursor.fetchone()
    conn.commit()
    if user is None:
        return None
    return User(user[0], user[9], user[10], user[11])


@app.route('/')
def welcome():
    one_year_ago = datetime.now() - relativedelta(years=1)
    # print(one_year_ago)
    cursor.execute(queries["welcome"], (one_year_ago,))
    interesting_answered_questions = cursor.fetchall()

    cursor.execute(queries["leaderboard"], (one_year_ago, one_year_ago, one_year_ago, one_year_ago, ))
    leaderboard = cursor.fetchall()

    form = SearchForm()

    return render_template('welcome.html', form=form,  interesting_answered_questions=interesting_answered_questions, leaderboard=leaderboard, title = "Interesting Questions")

@app.route('/navbar')
def navbar():

    form = SearchForm()
    return render_template('navbar.html', form=form)

@app.route('/unanswered_questions')
@login_required
def unanswered_questions():

    if current_user is None:
        return redirect(url_for('welcome'))

    cursor.execute(queries["unanswered_questions"], (current_user.id, ))
    unanswered_questions = cursor.fetchall()

    one_year_ago = datetime.now() - relativedelta(years=1)
    cursor.execute(queries["leaderboard"], (one_year_ago, one_year_ago, one_year_ago, one_year_ago, ))
    leaderboard = cursor.fetchall()

    form = SearchForm()

    #Keeping same name for interesting answered questions so that easy to handle in html
    return render_template('welcome.html', form=form,  interesting_answered_questions=unanswered_questions, leaderboard=leaderboard, title = "Unanswered Questions")

@app.route('/popular-tags', methods=['GET', 'POST'])
def popular_tags():

    if request.method == 'GET':
        cursor.execute(queries["popular_tags"])
        popular_tags = cursor.fetchall()
        return render_template('tags.html', popular_tags=popular_tags)

    # date = request.args.get('date')
    # get date from HTML form
    # print(request.form.keys())
    date = request.form.get('date')
    popular_tags = []
    popular_tags_by_date = []

    print(date)
    #convert date to type datetime
    if date:
    # "popular_tags_by_date": "With RelevantPosts AS (SELECT Id, Tags FROM posts WHERE PostTypeId = 1 AND CreationDate > %s) SELECT TagName, tags.Id, Count(*) AS Count FROM RelevantPosts, tags WHERE RelevantPosts.Tags LIKE '%' || tags.TagName || '%' GROUP BY TagName, tags.Id ORDER BY Count Desc LIMIT 20;"
        # date = datetime.strptime(date, '%Y-%m-%d')
        # print(date)
        cursor.execute(queries["popular_tags_by_date"].format(date))
        popular_tags_by_date = cursor.fetchall()
        print(popular_tags_by_date)
        

    cursor.execute(queries["popular_tags"])
    popular_tags = cursor.fetchall()
    request.form = None
    return render_template('tags.html', popular_tags=popular_tags, popular_tags_by_date=popular_tags_by_date)


@app.route('/admin-login')
def admin_login():

    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    
    form = AdminLoginForm()

    if form.validate_on_submit():
        cursor.execute(queries["check_admin"], (form.username.data, form.password.data, ))
        admin = cursor.fetchone()
        conn.commit()
        if admin is None:
            return redirect(url_for('admin_login'))
        
        cursor.execute(queries["get_admin_id"], (form.username.data, form.password.data, ))
        admin_id = cursor.fetchone()
        conn.commit()
        user = User(admin_id[0], form.username.data, form.password.data, None)
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('admin'))

    return render_template('admin.html', form=form)

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():

    cursor.execute(queries["check_admin"], (current_user.username, current_user.password, ))
    is_admin = cursor.fetchone()

    if is_admin is None:
        return redirect(url_for('welcome'))

    month = request.form.get('month')

    if month is None:
        return render_template('admin_dashboard.html', data=[])

    #Extract year and month from type month of HTML
    year = int(month[:4])
    month = int(month[5:])
    cursor.execute(queries["admin"], (year, month, ))
    data = cursor.fetchall()
    return render_template('admin_dashboard.html', signup_rates=data)

@app.route('/admin-delete-posts', methods=['GET', 'POST'])
def delete_posts():

    cursor.execute(queries["check_admin"], (current_user.username, current_user.password, ))
    is_admin = cursor.fetchone()
    if is_admin is None:
        return redirect(url_for('welcome'))
    
    score = request.form.get('score')
    if score is None:
        return render_template('admin_dashboard.html')
    
    score = int(score)
    cursor.execute(queries["admin_delete_posts"], (score,))
    conn.commit()

    return render_template('admin_dashboard.html')

@app.route('/profile')
@login_required
def profile():
    userid = current_user.id
    cursor.execute(queries["profile"], (userid, ))
    profile = cursor.fetchall()
    profile = profile[0]
    return render_template('profile.html', profile=profile)

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    
    form = ChangePasswordForm()

    if form.validate_on_submit():

        if(form.newpassword.data != form.confirmnewpassword.data):
            return redirect(url_for('change_password')), 401
        
        if(form.oldpassword.data != current_user.password):
            return redirect(url_for('change_password')), "Old password does not match"

        cursor.execute(queries["change_password"], (form.newpassword.data, current_user.id,))
        conn.commit()
        return redirect(url_for('profile'))
    
    return render_template('change_password.html', form=form)

@app.route('/login.html', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('welcome'))
    form = LoginForm()

    if form.validate_on_submit():
        cursor.execute(queries["login_check"], (form.username.data,  form.accid.data, form.password.data,))
        result = cursor.fetchone()

        if result is None:
            return redirect(url_for('login')), 401
        
        elif len(result) == 0:
            return redirect(url_for('login')), 401

        else:
            
            cursor.execute(queries["login"], (form.username.data,  form.accid.data, form.password.data,))
            conn.commit()

            #get userid
            cursor.execute(queries["get_userid"], (form.username.data,  form.accid.data, form.password.data,))
            userid = cursor.fetchone()[0]

            user = User(userid, form.username.data, form.password.data, form.accid.data)
            login_user(user)
            next_page = request.args.get('next')

            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('welcome')
            return redirect(next_page)

    elif request.method == 'POST':
        if form.username.data == None or form.password.data == None:
            return redirect(url_for('login'))
        else:
            cursor.execute(queries["login_check"], (form.username.data,  form.accid.data, form.password.data,))
            result = cursor.fetchall()

            if len(result) == 0:
                return redirect(url_for('login')), 401
            else:
                
                cursor.execute(queries["login"], (form.username.data,  form.accid.data, form.password.data,))
                conn.commit()

                #get userid
                cursor.execute(queries["get_userid"], (form.username.data,  form.accid.data, form.password.data,))
                userid = cursor.fetchone()[0]

                user = User(userid, form.username.data, form.password.data, form.accid.data)
                login_user(user)
                next_page = request.args.get('next')

                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('welcome')
                return redirect(next_page)
    
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('welcome')
    return render_template('login.html', title='Sign In', form=form, next_page=next_page)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('welcome'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if current_user.is_authenticated:
        return redirect(url_for('welcome')) 
    
    form = SignupForm()

    if form.validate_on_submit():
        try:
            cursor.execute(queries["signup"], (form.displayname.data, form.aboutme.data, form.location.data, form.websiteurl.data, form.password.data,))
            conn.commit()

            return redirect(url_for('login'))
        except Exception as e:
            print(e)
            return redirect(url_for('signup'))
    return render_template('signup.html', title='Sign Up', form=form)

@app.route('/users')
@login_required
def users():

    cursor.execute(queries["users_by_reputation"])
    users_reputation = cursor.fetchall()

    cursor.execute(queries["users_admin"])
    users_admin = cursor.fetchall()

    cursor.execute(queries["recommended_users"], (current_user.id, current_user.id, current_user.id, ))
    users_recommended = cursor.fetchall()

    return render_template('users.html', users_reputation=users_reputation, users_admin=users_admin, users_recommended=users_recommended)


@app.route('/user')
def user():
    userid = request.args.get('id')
    if userid == None:
        return redirect(url_for('profile'))
    #convert userid to int
    userid = int(userid)
    cursor.execute(queries["get_user"], (userid, ))
    user = cursor.fetchone()
    if(user == None):
        return render_template('404.html'), 404
    cursor.execute(queries["update_user_views"], (userid, ))
    conn.commit()

    # correct date format in user
    user = list(user)
    user[5] = user[5].strftime("%d %b %Y")
    user = tuple(user)


    one_year_ago = datetime.now() - relativedelta(years=1)
    cursor.execute(queries["leaderboard"], (one_year_ago, one_year_ago, one_year_ago, one_year_ago, ))
    leaderboard = cursor.fetchall()

    # print(leaderboard)

    #check followed
    followed = False
    if current_user.is_authenticated:
        cursor.execute(queries["check_followed"], (current_user.id, userid, ))
        followed = cursor.fetchone()
        if followed == None:
            followed = False
        else:
            followed = True

    return render_template('user.html', user=user, leaderboard=leaderboard, followed=followed)


@app.route('/question')
def question():
    qid = request.args.get('id')
    if qid == None:
        return render_template('404.html'), 404
    #convert qid to int
    qid = int(qid)
    cursor.execute(queries["similar_questions"].format(qid, qid))

    similar_questions = cursor.fetchall()
    cursor.execute(queries["question"], (qid, ))
    question = cursor.fetchone()

    if(question == None):
        return render_template('404.html'), 404
    
    cursor.execute(queries["update_viewcount"], (qid, ))
    conn.commit()

    acceptedanswerid = question[1]
    acceptedanswer = None
    aaid = -1
    comments_acceptedanswer = []
    if acceptedanswerid != None:
        cursor.execute(queries["accepted_answer"], (acceptedanswerid, ))
        acceptedanswer = cursor.fetchone()
        aaid = acceptedanswer[0]
        aaid = int(aaid)
        cursor.execute(queries["comments"], (aaid, ))
        comments_acceptedanswer = cursor.fetchall()

    cursor.execute(queries["answers"], (qid, aaid))
    answers = cursor.fetchall()

    cursor.execute(queries["comments"], (qid, ))
    comments_question = cursor.fetchall()

    for i in range(len(comments_question)):
        comments_question[i] = (comments_question[i][0], comments_question[i][1], comments_question[i][2], comments_question[i][3].strftime("%Y-%m-%d %H:%M:%S"))

    for i in range(len(answers)):
        cursor.execute(queries["comments"], (answers[i][0], ))
        comments_answer = cursor.fetchall()
        answers[i] = (answers[i], comments_answer)

    followed = False
    if current_user.is_authenticated:
        cursor.execute(queries["check_followed_post"], (current_user.id, qid, ))
        followed = cursor.fetchone()
        if followed == None:
            followed = False
        else:
            followed = True

    return render_template('question.html', question=question, acceptedanswer=acceptedanswer, answers=answers, comments_question=comments_question, comments_acceptedanswer=comments_acceptedanswer, similar_questions=similar_questions, followed=followed)

@app.route('/upvote', methods=['GET', 'POST'])
@login_required
def upvote():

    pid = request.args.get('id')
    if pid == None:
        return render_template('404.html'), 404
    #convert pid to int
    pid = int(pid)

    if request.method == 'GET':
        return redirect(url_for('question', id=pid))

    cursor.execute(queries["check_vote"], (current_user.id, pid, ))
    result = cursor.fetchall()
    if len(result) == 0:
        cursor.execute(queries["upvote"], (pid, current_user.id, ))
        conn.commit()
        cursor.execute(queries["increase_score"], (pid, ))
        conn.commit()
    else:
        if result[len(result) - 1][1] == 3:
            cursor.execute(queries["delete_vote"], (result[len(result) - 1][0],))
            conn.commit()
            cursor.execute(queries["increase_score"], (pid, ))
            conn.commit()

    
    return redirect(url_for('question', id=pid))

@app.route('/downvote', methods=['GET', 'POST'])
@login_required
def downvote():
    
        pid = request.args.get('id')
        if pid == None:
            return render_template('404.html'), 404
        #convert pid to int
        pid = int(pid)

        if request.method == 'GET':
            return redirect(url_for('question', id=pid))
    
        cursor.execute(queries["check_vote"], (current_user.id, pid, ))
        result = cursor.fetchall()
        if len(result) == 0:
            cursor.execute(queries["downvote"], (pid, current_user.id, ))
            conn.commit()
            cursor.execute(queries["decrease_score"], (pid, ))
            conn.commit()
        else:
            if result[len(result) - 1][1] == 2:
                cursor.execute(queries["delete_vote"], (result[len(result) - 1][0],))
                conn.commit()
                cursor.execute(queries["decrease_score"], (pid, ))
                conn.commit()
        return redirect(url_for('question', id=pid))

# #TODO
# @app.route('/acceptanswer' , methods=['POST'])
# @login_required
# def acceptanswer():
#     pid = request.args.get('id')
#     if pid == None:
#         return render_template('404.html'), 404
#     #convert pid to int
#     pid = int(pid)

#     cursor.execute(queries["get_post"], (pid,))
#     post = cursor.fetchone()
#     if post == None:
#         return render_template('404.html'), 404
    
#     if post[1] != 2:
#         return render_template('404.html'), 404
    


    # cursor.execute(queries["check_accepted_answer"], (pid, ))
    # result = cursor.fetchall()
    # if len(result) == 0:
    #     cursor.execute(queries["accept_answer"], (pid, ))
    #     conn.commit()
    #     cursor.execute(queries["increase_score"], (pid, ))
    #     conn.commit()
    # else:
    #     cursor.execute(queries["delete_accepted_answer"], (pid, ))
    #     conn.commit()
    #     cursor.execute(queries["decrease_score"], (pid, ))
    #     conn.commit()

    # return redirect(url_for('question', id=pid))


@app.route('/postquestion', methods=['GET', 'POST'])
@login_required
def postquestion():
    form = PostQuestionForm()

    if form.validate_on_submit():
        # Convert tags to a list of strings
        tags = form.tags.data.split()
        # print(tags)

        string_tags = ""
        for tag in tags:
            string_tags += "<" + tag + ">"

        for tag in tags:
            cursor.execute(queries["update_tag"], (tag, ))
            conn.commit()

        cursor.execute(queries["post_question"], (current_user.id, current_user.id, current_user.id, current_user.id, form.title.data, string_tags, form.body.data))
        conn.commit()

        cursor.execute(queries["get_question_id"], (current_user.id, form.title.data, form.body.data, string_tags))
        qid = cursor.fetchone()[0]
        conn.commit()

        return redirect(url_for('question', id=qid))
    
    return render_template('postquestion.html', title='Post Question', form=form)

#TODO: Check and then implement
@app.route('/postanswer', methods=['GET', 'POST'])
@login_required
def postanswer():

    pid = request.args.get('id')
    if pid == None:
        return render_template('404.html'), 404
    #convert pid to int
    pid = int(pid)

    if request.method == 'GET':
        return redirect(url_for('question', id=pid))

    cursor.execute(queries["get_post"], (pid, ))
    post = cursor.fetchone()
    if post == None:
        return render_template('403.html'), 404

    if post[1] != 1:
        return render_template('403.html'), 404

    form = request.form.get('message')
    if form == None:
        return render_template('404.html'), 404
    
    cursor.execute(queries["post_answer"], (current_user.id, current_user.id, pid, current_user.id, current_user.id, form))
    conn.commit()

    return redirect(url_for('question', id=pid))

    


@app.route('/editquestion', methods=['GET', 'POST'])
@login_required
def editquestion():

    pid = request.args.get('id')
    if pid == None:
        return render_template('404.html'), 404
    #convert pid to int
    pid = int(pid)

    cursor.execute(queries["get_post"], (pid, ))
    post = cursor.fetchone()
    if post == None:
        return render_template('404.html'), 405

    if post[1] != 1:
        return redirect(url_for('editanswer', id=pid))

    if post[2] != current_user.id:
        return render_template('401.html'), 401

    form = EditQuestionForm()

    if form.validate_on_submit():
        # print("Here1")
        cursor.execute(queries["edit_question"], (current_user.id, form.title.data, form.tags.data, form.body.data, pid,))
        conn.commit()
        # print("Here2")
        #Also need to update the posthistory table

        revision_uuid = uuid.uuid4()

        while(True):
            revision_uuid = str(revision_uuid)
            cursor.execute(queries["check_revision_uuid"], (revision_uuid,))
            result = cursor.fetchall()
            if len(result) == 0:
                break
            else:
                revision_uuid = uuid.uuid4()

        #convert uuid to string
        revision_uuid = str(revision_uuid)
        if(post[3] != form.title.data):
            cursor.execute(queries["update_posthistory"], (1, pid, revision_uuid, current_user.id, current_user.username, post[3],))
            conn.commit()

            cursor.execute(queries["update_posthistory"], (4, pid, revision_uuid, current_user.id, current_user.username, form.title.data,))
            conn.commit()

        if(post[4] != form.tags.data):
            cursor.execute(queries["update_posthistory"], (3, pid, revision_uuid, current_user.id, current_user.username, post[4],))
            conn.commit()

            cursor.execute(queries["update_posthistory"], (6, pid, revision_uuid, current_user.id, current_user.username, form.tags.data,))
            conn.commit()

        if(post[5] != form.body.data):
            cursor.execute(queries["update_posthistory"], (2, pid, revision_uuid, current_user.id, current_user.username, post[5],))
            conn.commit()

            cursor.execute(queries["update_posthistory"], (5, pid, revision_uuid, current_user.id, current_user.username, form.body.data,))
            conn.commit()

        return redirect(url_for('question', id=pid))
    
    form.title.data = post[3]
    form.tags.data = post[4]
    form.body.data = post[5]

    return render_template('editquestion.html', title='Edit Question', form=form, pid = pid)


#TODO
# @app.route('/editanswer', methods=['POST'])
# @login_required
# def editanswer():
    
#         pid = request.args.get('id')
#         if pid == None:
#             return render_template('404.html'), 404
#         #convert pid to int
#         pid = int(pid)
    
#         cursor.execute(queries["get_post"], (pid, ))
#         post = cursor.fetchone()
#         if post == None:
#             return render_template('404.html'), 404
    
#         if post[1] != 2:
#             return redirect(url_for('editquestion', id=pid))
    
#         if post[2] != current_user.id:
#             return render_template('401.html'), 401
    
#         form = EditAnswerForm()
    
#         if form.validate_on_submit():
#             cursor.execute(queries["edit_answer"], (current_user.id, form.body.data, pid,))
#             conn.commit()
    
#             #Also need to update the posthistory table

#             revision_uuid = uuid.uuid4()

#             while(True):
#                 cursor.execute(queries["check_revision_uuid"], (revision_uuid,))
#                 result = cursor.fetchall()
#                 if len(result) == 0:
#                     break
#                 else:
#                     revision_uuid = uuid.uuid4()

#             if(post[5] != form.body.data):
#                 cursor.execute(queries["update_posthistory"], (2, pid, revision_uuid, current_user.id, current_user.username, post[5],))
#                 conn.commit()

#                 cursor.execute(queries["update_posthistory"], (5, pid, revision_uuid, current_user.id, current_user.username, form.body.data,))
#                 conn.commit()

#             return redirect(url_for('question', id=pid))
        
#         form.body.data = post[5]

#         return render_template('editanswer.html', title='Edit Answer', form=form)


@app.route('/search_questions', methods=['GET', 'POST'])
def search_questions():
    
    form = SearchForm()

    if form.validate_on_submit():
        search = form.search.data

        search = '%' + search + '%'

        cursor.execute(queries["search_questions"], (search,))
        questions = cursor.fetchall()
        one_year_ago = datetime.now() - relativedelta(years=1)
        cursor.execute(queries["leaderboard"], (one_year_ago, one_year_ago, one_year_ago, one_year_ago, ))
        leaderboard = cursor.fetchall()

        return render_template('welcome.html', form=form,  interesting_answered_questions=questions, leaderboard=leaderboard, title = "Searched Questions")
    
    return redirect(url_for('welcome'))


@app.route('/revisions', methods=['GET', 'POST'])
def revisions():

    pid = request.args.get('id')
    if pid == None:
        return render_template('404.html'), 404
    #convert pid to int
    pid = int(pid)

    cursor.execute(queries["get_post"], (pid, ))
    post = cursor.fetchone()
    if post == None:
        return render_template('404.html'), 404
    
    cursor.execute(queries["get_posthistory"], (pid, ))
    posthistory = cursor.fetchall()

    return render_template('revisions.html', title='Revisions', posthistory=posthistory)


@app.route('/editprofile', methods=['GET', 'POST'])
@login_required
def editprofile():

    form = EditProfileForm()

    if form.validate_on_submit():

        cursor.execute(queries["edit_profile"], (form.aboutme.data, form.location.data, form.websiteurl.data, form.displayname.data, current_user.id, ))
        conn.commit()

        return redirect(url_for('profile', id=current_user.id))
    
    cursor.execute(queries["get_user"], (current_user.id, ))
    user = cursor.fetchone()
    if user == None:
        return render_template('404.html'), 404

    form.displayname.data = user[9]
    form.aboutme.data = user[6]
    form.websiteurl.data = user[8]
    form.location.data = user[7]

    return render_template('editprofile.html', title='Edit Profile', form=form)


@app.route('/followperson', methods=['POST'])
@login_required
def followperson():
    
    uid = request.args.get('id')
    if uid == None:
        return render_template('404.html'), 404
    #convert uid to int
    uid = int(uid)

    cursor.execute(queries["follow_person"], (current_user.id, uid,))
    conn.commit()

    return redirect(url_for('user', id=uid))

@app.route('/unfollowperson', methods=['POST'])
@login_required
def unfollowperson():
        
    uid = request.args.get('id')
    if uid == None:
        return render_template('404.html'), 404
    #convert uid to int
    uid = int(uid)

    cursor.execute(queries["unfollow_person"], (current_user.id, uid,))
    conn.commit()

    return redirect(url_for('user', id=uid))

@app.route('/getfollowersandfollowing', methods=['GET'])
def getfollowersandfollowing():
    
    uid = current_user.id

    cursor.execute(queries["get_followers"], (uid,))
    followers = cursor.fetchall()

    cursor.execute(queries["get_following"], (uid,))
    following = cursor.fetchall()

    return render_template('users.html', title='Followers', followers=followers, following=following)

@app.route('/followpost', methods=['GET','POST'])
@login_required
def followpost():
        
    pid = request.args.get('id')
    if pid == None:
        return render_template('404.html'), 404
    #convert pid to int
    pid = int(pid)

    cursor.execute(queries["follow_post"], (current_user.id, pid,))
    conn.commit()

    return redirect(url_for('question', id=pid))

@app.route('/unfollowpost', methods=['GET', 'POST'])
@login_required
def unfollowpost():

    pid = request.args.get('id')
    if pid == None:
        return render_template('404.html'), 404
    #convert pid to int
    pid = int(pid)

    cursor.execute(queries["unfollow_post"], (current_user.id, pid,))
    conn.commit()

    return redirect(url_for('question', id=pid))