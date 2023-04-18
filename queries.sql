--Stackoverflow database

--Check all (top 10) posts by a user
SELECT * FROM posts WHERE owneruserid = 5 LIMIT 10;

--Check all (top 10) posts by a user with a specific tag
SELECT * FROM posts WHERE owneruserid = 5 AND tags LIKE  '%<compilers>%' LIMIT 10;

--Create a new badge id, userid, class, name, tagbased, date
INSERT INTO badges (id, userid, class, name, tagbased, date) VALUES (1, 5, 1, 'Compiler', TRUE, '2018-01-01');

--Create a new vote for a post
INSERT INTO votes (id, postid, votetypeid, creationdate, userid) VALUES (1, 5, 1, '2018-01-01', 5);

--Create a new vote for a post with bounty amount
INSERT INTO votes (id, postid, votetypeid, creationdate, userid, bountyamount) VALUES (1, 5, 1, '2018-01-01', 5, 100);

--Create a new table Person_like_tag
CREATE TABLE Person_like_tag (
    person_id INT,
    tag_id INT,
    PRIMARY KEY (person_id, tag_id),
    FOREIGN KEY (person_id) REFERENCES users(id),
    FOREIGN KEY (tag_id) REFERENCES tags(id)
);

--Create a new table Person_follows_post
CREATE TABLE Person_follows_post (
    person_id INT,
    post_id INT,
    PRIMARY KEY (person_id, post_id),
    FOREIGN KEY (person_id) REFERENCES users(id),
    FOREIGN KEY (post_id) REFERENCES posts(id)
);

--Create a new table Person_follows_person
CREATE TABLE Person_follows_person (
    person_id INT,
    person_id_followed INT,
    PRIMARY KEY (person_id, person_id_followed),
    FOREIGN KEY (person_id) REFERENCES users(id),
    FOREIGN KEY (person_id_followed) REFERENCES users(id)
);

--Fetch all posts that a user has voted on
SELECT * FROM posts WHERE id IN (SELECT postid FROM votes WHERE userid = 5);

--Fetch all posts that a user has voted on with a specific tag
SELECT * FROM posts WHERE id IN (SELECT postid FROM votes WHERE userid = 5) AND tags LIKE  '%<compilers>%' LIMIT 10;

--Fetch all posts that a user follows
SELECT * FROM posts WHERE id IN (SELECT post_id FROM Person_follows_post WHERE person_id = 5);

--Fetch all tags that a user likes 
SELECT * FROM tags WHERE id IN (SELECT tag_id FROM Person_like_tag WHERE person_id = 5);

--Find latest posts that with the tag that user likes (Person_like_tag)
WITH v AS (SELECT person_id, tag_id FROM Person_like_tag WHERE person_id = 5),
t AS (SELECT tagname FROM tags WHERE id IN (SELECT tag_id FROM v)),
p AS (SELECT * FROM posts WHERE tags LIKE CONCAT('%<', t.tagname, '>%' ))
SELECT * FROM p ORDER BY p.creationdate DESC LIMIT 10;

--Find latest posts that with the tag that user likes (Person_like_tag) and user follows (Person_follows_post)
WITH v AS (SELECT person_id, tag_id FROM Person_like_tag WHERE person_id = 5),
t AS (SELECT tagname FROM tags WHERE id IN (SELECT tag_id FROM v)),
p AS (SELECT * FROM posts WHERE tags LIKE CONCAT('%<', t.tagname, '>%' ) AND id IN (SELECT post_id FROM Person_follows_post WHERE person_id = 5))
SELECT * FROM p ORDER BY p.creationdate DESC LIMIT 10;

--Retreive latest questions by a tag
SELECT * FROM posts WHERE tags LIKE  '%<compilers>%' AND posttypeid = 1 ORDER BY creationdate DESC LIMIT 10;

--Retreive all tags for a question
SELECT tags FROM posts WHERE id = 5;

--Add a new answer to a question
INSERT INTO posts (id, posttypeid, acceptedanswerid, parentid, creationdate, score, viewcount, body, owneruserid, ownerdisplayname, lasteditoruserid, lasteditordisplayname, lasteditdate, lastactivitydate, communityowneddate, closeddate, title, tags, answercount, commentcount, favoritecount, contentlicense) VALUES (1, 2, NULL, 5, '2018-01-01', 0, 0, 'This is an answer', 5, 'user5', NULL, NULL, NULL, '2018-01-01', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'CC BY-SA 2.5');

--Add a new comment to a question
INSERT INTO posts (id, posttypeid, acceptedanswerid, parentid, creationdate, score, viewcount, body, owneruserid, ownerdisplayname, lasteditoruserid, lasteditordisplayname, lasteditdate, lastactivitydate, communityowneddate, closeddate, title, tags, answercount, commentcount, favoritecount, contentlicense) VALUES (1, 2, NULL, 5, '2018-01-01', 0, 0, 'This is a comment', 5, 'user5', NULL, NULL, NULL, '2018-01-01', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'CC BY-SA 2.5');

--Add a new comment to an answer (Check this)
INSERT INTO posts (id, posttypeid, acceptedanswerid, parentid, creationdate, score, viewcount, body, owneruserid, ownerdisplayname, lasteditoruserid, lasteditordisplayname, lasteditdate, lastactivitydate, communityowneddate, closeddate, title, tags, answercount, commentcount, favoritecount, contentlicense) VALUES (1, 2, NULL, 5, '2018-01-01', 0, 0, 'This is a comment', 5, 'user5', NULL, NULL, NULL, '2018-01-01', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'CC BY-SA 2.5');

--Update "aboutme" for a user in users table
UPDATE users SET aboutme = 'I am a compiler expert' WHERE id = 5;


--Suggest new people to follow that I don't already follow based on common tags and lastaccessdate is latest
WITH v1 AS (SELECT person_id, tag_id FROM Person_like_tag WHERE person_id = 5),
v2 AS (SELECT person_id, tag_id FROM Person_like_tag WHERE person_id != 5 AND tag_id IN (SELECT tag_id FROM v1)),
v3 AS (SELECT DISTINCT person_id FROM v2 WHERE person_id NOT IN (SELECT person_id_followed FROM Person_follows_person WHERE person_id = 5)),
v4 AS (SELECT id, lastaccessdate FROM users WHERE id IN (SELECT person_id FROM v3) ORDER BY lastaccessdate DESC LIMIT 10),
v5 AS (SELECT id FROM v4)
SELECT * FROM users WHERE id IN (SELECT id FROM v5);


--account login and signup(if user does not exist already)
DECLARE username VARCHAR(255) = 'johndoe'
        accid INT = 99
        pass VARCHAR(255) = 'samplepass'
IF EXIST(SELECT * FROM users WHERE DisplayName = @username and (AccountId = @accid or Password = @pass) )
BEGIN
    Print 'User login successful'
    UPDATE users
    SET LastAccessDate = CURRENT_DATE
    WHERE DisplayName = @username and (AccountId = @accid or Password = @pass)
END
ELSE
BEGIN
    INSERT INTO users (AccountId, Reputation , Views, DownVotes,UpVotes, DisplayName, Location,WebsiteUrl, AboutMe, CreationDate ,LastAccessDate, Password) VALUES(@accid, 0, 0,0,0,@username , NULL, NULL,NULL,CURRENT_DATE,CURRENT_DATE , @pass )
END

--admin login
DECLARE adminname VARCHAR(255) = 'johndoe'
        pass VARCHAR(255) = 'samplepass'
IF EXIST(SELECT * FROM admins WHERE DisplayName = @adminname and Password = @pass)
BEGIN
    Print 'Admin login successful'
    UPDATE admins
    SET LastAccessDate = CURRENT_DATE
    WHERE  DisplayName = @adminname and Password = @pass
END
ELSE
BEGIN
    Print 'Admin sign up not permitted'
END



--new questions page
DECLARE owneruserid INTEGER := 99
        title TEXT := "sampletitle"
        contentlicense TEXT := "CC BY-SA 4.0"
        body TEXT := "samplebody"
        tagsss := ["tag1", "tag2", "tag3", "tag4"] 
FOR r in tagsss:
    UPDATE tags
    SET Count = Count + 1
    WHERE tags.TagName = r 
INSERT INTO posts(OwnerUserId,LastEditorUserId,PostTypeId,AcceptedAnswerId,Score,ParentId,ViewCount,AnswerCount
            ,CommentCount,OwnerDisplayName,LastEditorDisplayName,Title,Tags,ContentLicense,Body,FavoriteCount
            ,CreationDate,CommunityOwnedDate,ClosedDate,LastEditDate,LastActivityDate) VALUES
            (@owneruserid,@owneruserid,1,NULL,0,NULL,0,0,0, (SELECT DisplayName from users where Id = @owneruserid), 
            (SELECT DisplayName from users where Id = @owneruserid) , @title , @tagss , @contentlicense, @body , 
            NULL ,CURRENT_DATE ,NULL ,NULL , CURRENT_DATE , CURRENT_DATE );


-- get person who has answered your question with number
-- answer of a post is post and PostTypeID indicates it is an answer. 1 is question, 2 is answer


--helpers
SET User1id =1;
SELECT post2.OwnerUserId, COUNT(post2.OwnerUserId) AS answerCount
FROM (SELECT * FROM posts WHERE OwnerUserId = "X" AND PostTypeId = 1) AS post1
JOIN (SELECT * FROM posts WHERE PostTypeId = 2) AS post2
ON post1.Id = post2.ParentId
GROUP BY post2.OwnerUserId
ORDER BY answerCount DESC;
LIMIT 100;


-- get the questions of your helpers

With helpers as (
SELECT post2.OwnerUserId, COUNT(post2.OwnerUserId) AS answerCount
FROM (SELECT * FROM posts WHERE OwnerUserId = "X" AND PostTypeId = 1) AS post1
JOIN (SELECT * FROM posts WHERE PostTypeId = 2) AS post2
ON post1.Id = post2.ParentId
GROUP BY post2.OwnerUserId
ORDER BY answerCount DESC
LIMIT 100
)
SELECT Id FROM posts WHERE OwnerUserId in (SELECT OwnerUserId FROM helpers) AND PostTypeId = 1
ORDER BY CreationDate DESC;

-- Get the users according to accepted answer count from a given date

WITH acceptedAnswerCount AS ( 
SELECT post2.OwnerUserId, COUNT(post2.OwnerUserId) AS answerCount 
FROM (
SELECT ParentId, Id, OwnerUserId FROM posts WHERE PostTypeId = 2 AND CreationDate > '2019-01-01') AS post2 
INNER JOIN (SELECT Id, AcceptedAnswerId, OwnerUserId FROM posts WHERE PostTypeId = 1) AS post1 
ON post2.ParentId = post1.Id WHERE post2.Id = post1.AcceptedAnswerId 
GROUP BY post2.OwnerUserId 
ORDER BY answerCount DESC 
LIMIT 100 ) 
SELECT DisplayName, Id, answerCount 
FROM users 
INNER JOIN acceptedAnswerCount 
ON users.Id = acceptedAnswerCount.OwnerUserId 
ORDER BY answerCount DESC;

--Get the users leaderboard according to value = accepted answer count*40 + answer count*10 + question count*5 + comment count*1

WITH acceptedAnswerCount AS (
SELECT post2.OwnerUserId, COUNT(post2.OwnerUserId) AS answerCount
FROM (
SELECT ParentId, Id, OwnerUserId FROM posts WHERE PostTypeId = 2 AND CreationDate > '2019-01-01') AS post2
INNER JOIN (SELECT Id, AcceptedAnswerId, OwnerUserId FROM posts WHERE PostTypeId = 1) AS post1
ON post2.ParentId = post1.Id WHERE post2.Id = post1.AcceptedAnswerId
GROUP BY post2.OwnerUserId

), 
answerCount AS (
SELECT post2.OwnerUserId, COUNT(post2.OwnerUserId) AS answerCount
FROM Posts AS post2 WHERE post2.PostTypeId = 2 AND post2.CreationDate > '2019-01-01'
GROUP BY post2.OwnerUserId

),
questionCount AS (
SELECT OwnerUserId, COUNT(OwnerUserId) AS questionCount
FROM posts
WHERE PostTypeId = 1 AND CreationDate > '2019-01-01'
GROUP BY OwnerUserId
),
commentCount AS (
SELECT UserId, COUNT(UserId) AS commentCount
FROM comments
WHERE CreationDate > '2019-01-01'
GROUP BY UserId
)
,
totalScore AS (
SELECT acceptedAnswerCount.OwnerUserId, acceptedAnswerCount.answerCount*40 + answerCount.answerCount*10 + questionCount.questionCount*5 + commentCount.commentCount AS totalScore
FROM acceptedAnswerCount, answerCount, questionCount, commentCount
WHERE acceptedAnswerCount.OwnerUserId = answerCount.OwnerUserId AND acceptedAnswerCount.OwnerUserId = questionCount.OwnerUserId AND acceptedAnswerCount.OwnerUserId = commentCount.UserId
ORDER BY totalScore DESC
)
SELECT DisplayName, Id, totalScore  
FROM users
INNER JOIN totalScore
ON users.Id = totalScore.OwnerUserId
ORDER BY totalScore DESC;


-- votes for a given post.
WITH upvoteCount AS (
SELECT Count(*) AS upvoteCount
FROM votes
WHERE PostId = :postId AND VoteTypeId = 2
),
downvoteCount AS (
SELECT Count(*) AS downvoteCount
FROM votes
WHERE PostId = :postId AND VoteTypeId = 3
)
SELECT upvoteCount, downvoteCount
FROM upvoteCount, downvoteCount;

-- Get the most interesting answered questions based on the score, reputation of asker, upvotes and downvotes of the answer

WITH RelevantPosts 
AS ( SELECT Id, Score, OwnerUserId 
FROM posts 
WHERE PostTypeId = 1 AND CreationDate > '2019-01-01' AND AcceptedAnswerId IS NOT NULL )
,upvoteCount AS 
( 
SELECT RP.Id, RP.Score, RP.OwnerUserId, Count(*) AS upvoteCount     
FROM RelevantPosts AS RP 
LEFT OUTER JOIN (
    SELECT PostId, VoteTypeId 
    FROM votes 
    WHERE VoteTypeId = 2)AS V     
ON RP.Id = V.PostId     
GROUP BY RP.Id, RP.score, RP.owneruserid )
,downvoteCount AS 
(     
SELECT RP.Id, RP.Score, RP.OwnerUserId, Count(*) AS downvoteCount     
FROM RelevantPosts AS RP 
LEFT OUTER JOIN (
    SELECT PostId, VoteTypeId 
    FROM votes 
    WHERE VoteTypeId = 3) AS V     
ON RP.Id = V.PostId     
GROUP BY RP.Id, RP.score, RP.owneruserid )
,
AllVotes AS(
SELECT upvoteCount.Id, upvoteCount.Score, upvoteCount.OwnerUserId, upvoteCount.upvoteCount, downvoteCount.downvoteCount
FROM upvoteCount, downvoteCount
WHERE upvoteCount.Id = downvoteCount.Id
)

SELECT AllVotes.Id, users.Reputation/10 + AllVotes.upvoteCount*10 + AllVotes.downvoteCount*10 + AllVotes.Score*50 AS totalScore
FROM AllVotes, users
WHERE AllVotes.OwnerUserId = users.Id
ORDER BY totalScore DESC
LIMIT 100;




-- . To fetch the tags with the most questions all time
SELECT TagName, Id, Count FROM tags
ORDER BY Count Desc LIMIT 20;

-- To fetch the tags with with the most questions after :date
With RelevantPosts AS (
    SELECT Id, Tags
    FROM posts
    WHERE PostTypeId = 1 AND CreationDate > 
)
SELECT TagName, tags.Id, Count(*) AS Count
FROM RelevantPosts, tags
WHERE RelevantPosts.Tags LIKE '%' || tags.TagName || '%'
GROUP BY TagName, tags.Id
ORDER BY Count Desc LIMIT 20;


--get tags of a question
SELECT *
FROM (
    SELECT regexp_split_to_table(tags, '[><]') AS tag
    FROM posts
    WHERE Id = 2
) AS tags where tag != '';



--to fetch the questions similar to the given question based on the tags

WITH tagsForGivenQuestion AS (
SELECT *
FROM (
    SELECT regexp_split_to_table(tags, '[><]') AS tag
    FROM posts
    WHERE Id = :questionId
) AS tags WHERE tag !='';
)
SELECT posts.Id, count(*) AS count
FROM posts, tagsForGivenQuestion
WHERE posts.Tags LIKE '%' || tagsForGivenQuestion.tag || '%'
AND posts.Id != :questionId
GROUP BY posts.Id
ORDER BY count DESC
LIMIT 10;

--upvote
INSERT INTO votes (Id, PostId, 2, CreationDate, UserId, BountyAmount)
VALUES (:id, :postId, CURRENT_DATE, :userId, :bountyAmount);
--downvote
INSERT INTO votes (Id, PostId, 3, CreationDate, UserId, BountyAmount)
VALUES (:id, :postId, CURRENT_DATE, :userId, :bountyAmount);



--gold badges : list of people 
with t1(personid , ansid) as
(
    select a.OwnerUserId , a.Id
    from posts a 
    where a.PostTypeId = 2
),
    t2(personid, ansid) as
(
    select personid , ansid
    from t1 , posts b
    where ansid = b.AcceptedAnswerId
),
    t3(personid, countans) as
(
    select personid, count(ansid)
    from t2
    group by personid
)
    select personid from t3 where countans >= 50;




