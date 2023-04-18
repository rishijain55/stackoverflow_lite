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
IF EXIST(SELECT * FROM users WHERE UserID = @username and (AccountId = @accid or Password = @pass) )
BEGIN
    Print 'User login successful'
END
ELSE
BEGIN
    INSERT INTO users (AccountId, Reputation , Views, DownVotes,UpVotes, DisplayName, Location,WebsiteUrl, AboutMe, CreationDate ,LastAccessDate, Password) VALUES(@accid, 0, 0,0,0,@username , NULL, NULL,NULL,CURRENT_DATE,CURRENT_DATE , @pass )
END





