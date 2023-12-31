BEGIN TRANSACTION;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
  Id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  AccountId INT ,
  Reputation INT NOT NULL,
  Views INT NOT NULL,
  DownVotes INT NOT NULL,
  UpVotes INT NOT NULL,
  DisplayName VARCHAR(255) NOT NULL,
  Location VARCHAR(255),
  WebsiteUrl VARCHAR(255),
  AboutMe TEXT,
  CreationDate TIMESTAMP NOT NULL,
  LastAccessDate TIMESTAMP NOT NULL
);

DROP TABLE IF EXISTS admins;
CREATE TABLE admins (
    Id INT NOT NULL PRIMARY KEY ,
    DisplayName VARCHAR(255) NOT NULL,
    WebsiteUrl VARCHAR(255) ,
    CreationDate TIMESTAMP NOT NULL,
    LastAccessDate TIMESTAMP NOT NULL,
    Password VARCHAR(255) NOT NULL
);

DROP TABLE IF EXISTS badges;
CREATE TABLE badges (
  Id INT NOT NULL PRIMARY KEY,
  UserId INT NOT NULL REFERENCES users(Id) ON DELETE CASCADE,
  Class INT NOT NULL,
  Name VARCHAR(255) NOT NULL,
  TagBased BOOLEAN NOT NULL,
  Date TIMESTAMP NOT NULL
);


DROP TABLE IF EXISTS comments;
CREATE TABLE comments (
  Id INT NOT NULL PRIMARY KEY,
  PostId INT NOT NULL REFERENCES posts(Id) ON DELETE CASCADE,
  UserId INT REFERENCES users(Id) ON DELETE CASCADE,
  --If userid doesn't exist, then the user commented as a guest.
  --She needs name and email, but email is not included in public data for privacy reasons. 
  Score INT NOT NULL,
  ContentLicense VARCHAR(20),
  UserDisplayName VARCHAR(255) ,
  Text TEXT NOT NULL,
  CreationDate TIMESTAMP NOT NULL
);

DROP TABLE IF EXISTS post_history;
CREATE TABLE post_history (
  Id INT NOT NULL PRIMARY KEY,
  PostId INT NOT NULL REFERENCES posts(Id) ON DELETE CASCADE,
  UserId INT REFERENCES users(Id),
  PostHistoryTypeId INT NOT NULL,
  UserDisplayName VARCHAR(255) ,
  ContentLicense VARCHAR(20),
  RevisionGUID VARCHAR(36) NOT NULL,
  Text TEXT ,
  Comment TEXT,
  CreationDate TIMESTAMP NOT NULL

);

DROP TABLE IF EXISTS post_links;
CREATE TABLE post_links (
  Id INT NOT NULL PRIMARY KEY,
  RelatedPostId INT NOT NULL REFERENCES posts(Id) ON DELETE CASCADE,
  PostId INT NOT NULL REFERENCES posts(Id) ON DELETE CASCADE,
  LinkTypeId INT NOT NULL,
  CreationDate TIMESTAMP NOT NULL

);

DROP TABLE IF EXISTS posts;
CREATE TABLE posts (
  Id INTEGER NOT NULL PRIMARY KEY,
  OwnerUserId INTEGER REFERENCES users(Id),
  LastEditorUserId INTEGER REFERENCES users(Id),
  PostTypeId INTEGER NOT NULL,
  AcceptedAnswerId INTEGER REFERENCES posts(Id),
  Score INTEGER NOT NULL,
  ParentId INTEGER REFERENCES posts(Id) ON DELETE CASCADE,
  ViewCount INTEGER,
  AnswerCount INTEGER,
  CommentCount INTEGER,
  OwnerDisplayName TEXT,
  LastEditorDisplayName TEXT,
  Title TEXT,
  Tags TEXT,
  ContentLicense TEXT,
  Body TEXT,
  FavoriteCount INTEGER,
  CreationDate TIMESTAMP NOT NULL,
  CommunityOwnedDate TIMESTAMP,
  ClosedDate TIMESTAMP,
  LastEditDate TIMESTAMP,
  LastActivityDate TIMESTAMP NOT NULL
);

DROP TABLE IF EXISTS tags;
CREATE TABLE tags (
    Id INTEGER NOT NULL PRIMARY KEY,
    ExcerptPostId INTEGER ,
    WikiPostId INTEGER ,
    TagName VARCHAR(50) NOT NULL,
    Count INTEGER NOT NULL
);

DROP TABLE IF EXISTS votes;
CREATE TABLE votes (
    Id INT NOT NULL PRIMARY KEY,
    UserId INT  REFERENCES users(Id) ON DELETE CASCADE,
    PostId INT NOT NULL REFERENCES posts(Id) ON DELETE CASCADE,
    VoteTypeId INT NOT NULL,
    BountyAmount INT ,
    CreationDate TIMESTAMP NOT NULL
);

--Create a new table Person_like_tag
DROP TABLE IF EXISTS Person_like_tag;
CREATE TABLE Person_like_tag (
    person_id INT,
    tag_id INT,
    PRIMARY KEY (person_id, tag_id),
    FOREIGN KEY (person_id) REFERENCES users(id),
    FOREIGN KEY (tag_id) REFERENCES tags(id)
);

--Create a new table Person_follows_post
DROP TABLE IF EXISTS Person_follows_post;
CREATE TABLE Person_follows_post (
    person_id INT,
    post_id INT,
    PRIMARY KEY (person_id, post_id),
    FOREIGN KEY (person_id) REFERENCES users(id),
    FOREIGN KEY (post_id) REFERENCES posts(id)
);

--Create a new table Person_follows_person
DROP TABLE IF EXISTS Person_follows_person;
CREATE TABLE Person_follows_person (
    person_id INT,
    person_id_followed INT,
    PRIMARY KEY (person_id, person_id_followed),
    FOREIGN KEY (person_id) REFERENCES users(id),
    FOREIGN KEY (person_id_followed) REFERENCES users(id)
);


END TRANSACTION;
