queries = {
    "welcome": '''
        WITH RelevantPosts 
        AS ( SELECT Id, Score, OwnerUserId 
        FROM posts 
        WHERE PostTypeId = 1 AND CreationDate > %s AND AcceptedAnswerId IS NOT NULL 
        ),
        
        upvoteCount AS 
        ( 
        SELECT RP.Id, RP.Score, RP.OwnerUserId, Count(*) AS upvoteCount     
        FROM RelevantPosts AS RP 
        LEFT OUTER JOIN (
            SELECT PostId, VoteTypeId 
            FROM votes 
            WHERE VoteTypeId = 2)AS V     
        ON RP.Id = V.PostId     
        GROUP BY RP.Id, RP.score, RP.owneruserid 
        ),
        
        downvoteCount AS 
        (     
        SELECT RP.Id, RP.Score, RP.OwnerUserId, Count(*) AS downvoteCount     
        FROM RelevantPosts AS RP 
        LEFT OUTER JOIN (
            SELECT PostId, VoteTypeId 
            FROM votes 
            WHERE VoteTypeId = 3) AS V     
        ON RP.Id = V.PostId     
        GROUP BY RP.Id, RP.score, RP.owneruserid 
        ),
        
        AllVotes AS(
        SELECT upvoteCount.Id, upvoteCount.Score, upvoteCount.OwnerUserId, upvoteCount.upvoteCount, downvoteCount.downvoteCount
        FROM upvoteCount, downvoteCount
        WHERE upvoteCount.Id = downvoteCount.Id
        ),
        
        PostIds AS (
        SELECT AllVotes.Id, users.Reputation/10 + AllVotes.upvoteCount*10 + AllVotes.downvoteCount*10 + AllVotes.Score*50 AS totalScore
        FROM AllVotes, users
        WHERE AllVotes.OwnerUserId = users.Id
        ORDER BY totalScore DESC
        LIMIT 100
        ),

        Final AS (
        SELECT posts.title, users.displayname, posts.tags, posts.answercount, posts.score, posts.id
        FROM posts, users
        WHERE posts.Id IN (SELECT Id FROM PostIds) AND posts.OwnerUserId = users.Id AND posts.PostTypeId = 1 AND posts.acceptedanswerid IS NOT NULL
        
        )

        SELECT * FROM Final;
    ''',
        # change score to 0 if null
        # acceptanswerid should be null

    "leaderboard": '''

        WITH acceptedAnswerCount AS (
        SELECT post2.OwnerUserId, COUNT(post2.OwnerUserId) AS answerCount
        FROM (
        SELECT ParentId, Id, OwnerUserId FROM posts WHERE PostTypeId = 2 AND CreationDate > %s) AS post2
        INNER JOIN (SELECT Id, AcceptedAnswerId, OwnerUserId FROM posts WHERE PostTypeId = 1) AS post1
        ON post2.ParentId = post1.Id WHERE post2.Id = post1.AcceptedAnswerId
        GROUP BY post2.OwnerUserId 
        ), 
        
        answerCount AS (
        SELECT post2.OwnerUserId, COUNT(post2.OwnerUserId) AS answerCount
        FROM Posts AS post2 WHERE post2.PostTypeId = 2 AND post2.CreationDate > %s
        GROUP BY post2.OwnerUserId
        ),
        
        questionCount AS (
        SELECT OwnerUserId, COUNT(OwnerUserId) AS questionCount
        FROM posts
        WHERE PostTypeId = 1 AND CreationDate > %s
        GROUP BY OwnerUserId
        ),
        
        commentCount AS (
        SELECT UserId, COUNT(UserId) AS commentCount
        FROM comments
        WHERE CreationDate > %s
        GROUP BY UserId
        ),
        
        totalScore AS (
        SELECT acceptedAnswerCount.OwnerUserId, acceptedAnswerCount.answerCount*40 + answerCount.answerCount*10 + questionCount.questionCount*5 + commentCount.commentCount AS score
        FROM acceptedAnswerCount, answerCount, questionCount, commentCount
        WHERE acceptedAnswerCount.OwnerUserId = answerCount.OwnerUserId AND acceptedAnswerCount.OwnerUserId = questionCount.OwnerUserId AND acceptedAnswerCount.OwnerUserId = commentCount.UserId
        ORDER BY score DESC
        )
        
        SELECT DisplayName, Id, score  
        FROM users
        INNER JOIN totalScore
        ON users.Id = totalScore.OwnerUserId
        ORDER BY score DESC; 
    ''',

    "popular_tags": '''
        SELECT TagName, Id, Count FROM tags
        ORDER BY Count Desc LIMIT 20;
    ''',

    # "popular_tags_by_date": "With RelevantPosts AS (SELECT id, regexp_split_to_table(tags, '[><]') AS tag FROM posts WHERE PostTypeId = 1 AND CreationDate > '{0}'), a AS (SELECT id, count(*) FROM RelevantPosts GROUP BY id ORDER BY count DESC LIMIT 20) SELECT TagName, tags.Id, a.count FROM a, tags WHERE a.id = tags.id;"
    "popular_tags_by_date": '''
        WITH RelevantPosts AS (
        SELECT regexp_split_to_table(tags, '[><]') AS tag FROM posts WHERE PostTypeId = 1 AND CreationDate > '{0}'
        ), temp AS (
        SELECT tag FROM RelevantPosts WHERE tag != ''
        ), 
        a AS (
        SELECT tag, count(*) FROM RelevantPosts GROUP BY tag ORDER BY count DESC LIMIT 20
        ) 
        SELECT TagName, id, a.count FROM a, tags WHERE a.tag = tags.tagname ORDER BY count DESC;
    ''',

    "admin": '''
        WITH a AS (
        select EXTRACT(Year FROM CreationDate)::INTEGER AS year, 
       EXTRACT(Month FROM CreationDate)::INTEGER AS month
        from Users WHERE EXTRACT(Year FROM CreationDate) >= %s AND EXTRACT(Month FROM CreationDate) >= %s)
        SELECT year, month, count(*) as users FROM a GROUP BY year, month ORDER BY year, month ASC;
    ''',

    "check_admin": '''
        SELECT id FROM admins WHERE displayname = %s AND password = %s;
    ''',

    "get_admin_id": '''
        SELECT id FROM admins WHERE displayname = %s AND password = %s;
    ''',
    
    "admin_delete_posts": '''
        DELETE
        FROM posts 
        WHERE score <= %s;
    ''',

    "profile": '''
        SELECT id, reputation, views, upvotes, downvotes, creationdate, aboutme, location, websiteurl, displayname, password, accountid FROM users
        WHERE users.id = %s;
    ''',

    "login_check": '''
        SELECT * FROM users WHERE DisplayName = %s and (AccountId = %s or Password = %s);
    ''',

    "login": '''
        UPDATE users
        SET LastAccessDate = CURRENT_DATE
        WHERE DisplayName = %s and (AccountId = %s or Password = %s);
    ''',

    "get_userid": '''
        SELECT Id FROM users WHERE DisplayName = %s and (AccountId = %s or Password = %s);
    ''',

    "unanswered_questions": '''
        With helpers as (
        SELECT post2.OwnerUserId, COUNT(post2.OwnerUserId) AS answerCount
        FROM (SELECT * FROM posts WHERE OwnerUserId = %s AND PostTypeId = 1) AS post1
        JOIN (SELECT * FROM posts WHERE PostTypeId = 2) AS post2
        ON post1.Id = post2.ParentId
        GROUP BY post2.OwnerUserId
        ORDER BY answerCount DESC
        LIMIT 100
        ),

        temp as (
        SELECT id, title, tags, answercount, score, owneruserid FROM posts WHERE OwnerUserId in (SELECT OwnerUserId FROM helpers) AND PostTypeId = 1
        ORDER BY CreationDate DESC
        )

        SELECT title, displayname, tags, answercount, score, temp.id
        FROM temp, users
        WHERE temp.OwnerUserId = users.Id
        ORDER BY CreationDate DESC;

    ''',

    "signup": '''
        INSERT INTO users (DisplayName, AboutMe, Location, WebsiteUrl, Views, UpVotes, DownVotes, CreationDate, LastAccessDate, Reputation, Password) 
        VALUES (%s, %s, %s, %s, 0, 0, 0, CURRENT_DATE, CURRENT_DATE, 1, %s);
    ''',

    "similar_questions": "WITH tagsForGivenQuestion AS (SELECT * FROM (SELECT regexp_split_to_table(tags, '[><]') AS tag FROM posts WHERE Id = {0}) AS tags WHERE tag IS NOT NULL), a AS (SELECT posts.Id, count(*) AS count FROM posts, tagsForGivenQuestion WHERE posts.Tags LIKE '%' || tagsForGivenQuestion.tag || '%' AND posts.Id != {1} AND posts.PostTypeId = 1 GROUP BY posts.Id ORDER BY count DESC LIMIT 10) SELECT id, title, tags FROM posts WHERE Id IN (SELECT Id FROM a);",

    "question": '''
        SELECT id, acceptedanswerid, score, viewcount, title, tags, body, parentid FROM posts WHERE Id = %s;
    ''',

    "update_viewcount": '''
        UPDATE posts
        SET viewcount = viewcount + 1
        WHERE Id = %s;
    ''',

    "accepted_answer" : '''
        SELECT id, score, body FROM posts WHERE Id = %s;
    ''',

    "answers": '''
        SELECT id, score, body FROM posts WHERE ParentId = %s AND PostTypeId = 2 AND id != %s;
    ''',

    "comments": '''
        SELECT id, userid, text, creationdate from comments WHERE PostId = %s;
    ''',

    "get_user": '''
        SELECT id, reputation, views, upvotes, downvotes, creationdate, aboutme, location, websiteurl, displayname FROM users WHERE id = %s;
    ''',

    "update_user_views": '''
        UPDATE users
        SET views = views + 1
        WHERE id = %s;
    ''',

    "check_vote": '''
        SELECT id, votetypeid FROM votes WHERE userid = %s AND postid = %s;
    ''',

    "upvote": '''
        INSERT INTO votes (PostId, VoteTypeId, CreationDate, UserId) VALUES (%s, 2, CURRENT_DATE, %s);
    ''',

    "downvote": '''
        INSERT INTO votes (PostId, VoteTypeId, CreationDate, UserId) VALUES (%s, 3, CURRENT_DATE, %s);
    ''',

    "delete_vote": '''
        DELETE FROM votes WHERE id = %s;
    ''',

    "increase_score": '''
        UPDATE posts
        SET score = score + 1
        WHERE id = %s;
    ''',
    "decrease_score": '''
        UPDATE posts
        SET score = score - 1
        WHERE id = %s;
    ''',

    "update_tag": '''
        UPDATE tags
        SET Count = Count + 1
        WHERE tags.TagName = %s;
    ''',

    "post_question": '''
        INSERT INTO posts(OwnerUserId, LastEditorUserId, PostTypeId, AcceptedAnswerId, Score, ParentId, ViewCount, AnswerCount, CommentCount, OwnerDisplayName, LastEditorDisplayName, Title, Tags, Body, FavoriteCount, CreationDate, CommunityOwnedDate, ClosedDate, LastEditDate, LastActivityDate) 
        VALUES
        (%s, %s,1,NULL,0,NULL,0,0,0, (SELECT DisplayName from users where Id = %s),(SELECT DisplayName from users where Id = %s) , %s , %s , %s, NULL ,CURRENT_DATE ,NULL ,NULL , CURRENT_DATE , CURRENT_DATE );
    ''',

    "change_password": '''
        UPDATE users
        SET Password = %s
        WHERE id = %s;
    ''',

    "search_questions": '''
        WITH
            a AS (SELECT posts.title, posts.tags, posts.answercount, posts.score, posts.id, posts.owneruserid FROM posts WHERE posts.posttypeid = 1 AND posts.title ILIKE %s AND posts.owneruserid IS NOT NULL)

        SELECT a.title, users.displayname, a.tags, a.answercount, a.score, a.id FROM a, users WHERE a.owneruserid = users.id LIMIT 50;
    ''',

    "edit_profile": '''
        UPDATE users
        SET AboutMe = %s, Location = %s, WebsiteUrl = %s, LastAccessDate = CURRENT_DATE, DisplayName = %s
        WHERE id = %s;
    ''',

    "get_post": '''
        SELECT id, posttypeid, owneruserid, title, tags, body FROM posts WHERE id = %s;
    ''',

    "edit_question": '''
        UPDATE posts
        SET lasteditoruserid = %s, title = %s, tags = %s, body = %s, lasteditdate = CURRENT_DATE
        WHERE id = %s;
    ''',

    "edit_answer": '''
        UPDATE posts
        SET lasteditoruserid = %s, body = %s, lasteditdate = CURRENT_DATE
        WHERE id = %s;
    ''',

    "update_posthistory": '''
        INSERT INTO post_history (PostHistoryTypeId, PostId, RevisionGUID, CreationDate, UserId, UserDisplayName, Text)
        VALUES (%s, %s, %s, CURRENT_DATE, %s, %s, %s);
    ''',

    "check_revision_uuid": '''
        SELECT id FROM post_history WHERE RevisionGUID = %s;
    ''',    

    "follow_person": '''
        INSERT INTO Person_follows_person(person_id, person_id_followed)
        VALUES (%s, %s);
    ''',

    "unfollow_person": '''
        DELETE FROM Person_follows_person WHERE person_id = %s AND person_id_followed = %s;
    ''',

    "check_followed": '''
        SELECT person_id, person_id_followed FROM Person_follows_person WHERE person_id = %s AND person_id_followed = %s;
    ''',

    "get_followers": '''
        WITH a AS (SELECT person_id FROM Person_follows_person WHERE person_id_followed = %s)
        SELECT displayname, id FROM users, a WHERE users.id = a.person_id;
    ''',

    "get_following": '''
        WITH a AS (SELECT person_id_followed FROM Person_follows_person WHERE person_id = %s)
        SELECT displayname, id FROM users, a WHERE users.id = a.person_id_followed;
    ''',

    "get_question_id": '''
        SELECT id FROM posts WHERE owneruserid = %s AND title = %s AND body = %s AND tags = %s;
    ''',

    "users_by_reputation": '''
        SELECT displayname, id, reputation FROM users ORDER BY reputation DESC LIMIT 10;
    ''',

    "users_admin": '''
        SELECT displayname, id FROM admins LIMIT 10;
    ''',

    "recommended_users": '''
        WITH v1 AS 
    (
        SELECT person_id, tag_id FROM Person_like_tag WHERE person_id = %s
    ),

    v2 AS 
    (
        SELECT person_id, tag_id FROM Person_like_tag WHERE person_id != %s AND tag_id IN (SELECT tag_id FROM v1)
    ),
    
    v3 AS 
    (
        SELECT DISTINCT person_id FROM v2 WHERE person_id NOT IN (SELECT person_id_followed FROM Person_follows_person WHERE person_id = %s)
    ),
    
    v4 AS 
    (
        SELECT id, lastaccessdate FROM users WHERE id IN (SELECT person_id FROM v3) ORDER BY lastaccessdate DESC LIMIT 10
    ),
    
    v5 AS 
    (
        SELECT id FROM v4
    )
    
    SELECT displayname, id FROM users 
    WHERE id IN (SELECT id FROM v5);
    ''',

    "get_posthistory": ''' 
        SELECT id, posthistorytypeid, postid, revisionguid, creationdate, userid, userdisplayname, text FROM post_history WHERE postid = %s;
    ''',

    "follow_post": '''
        INSERT INTO Person_follows_post(person_id, post_id)
        VALUES (%s, %s);
    ''',

    "unfollow_post": '''
        DELETE FROM Person_follows_post WHERE person_id = %s AND post_id = %s;
    ''',

    "check_followed_post": '''
        SELECT person_id, post_id FROM Person_follows_post WHERE person_id = %s AND post_id = %s;
    ''',

    "post_answer": '''
        INSERT INTO posts( OwnerUserId, LastEditorUserId, PostTypeId, AcceptedAnswerId, Score, ParentId, ViewCount, AnswerCount, CommentCount, OwnerDisplayName, LastEditorDisplayName, Title, Tags, Body, FavoriteCount, CreationDate, CommunityOwnedDate, ClosedDate, LastEditDate, LastActivityDate)
        VALUES
        (%s, %s,2,NULL,0,%s,0,0,0, (SELECT DisplayName from users where Id = %s),(SELECT DisplayName from users where Id = %s) , NULL , NULL , %s, NULL ,CURRENT_DATE ,NULL ,NULL , CURRENT_DATE , CURRENT_DATE );
    ''',

}