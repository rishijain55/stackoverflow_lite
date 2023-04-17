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

DROP TABLE IF EXISTS badges;
CREATE TABLE badges (
  Id INT NOT NULL PRIMARY KEY,
  UserId INT NOT NULL REFERENCES users(Id),
  Class INT NOT NULL,
  Name VARCHAR(255) NOT NULL,
  TagBased BOOLEAN NOT NULL,
  Date TIMESTAMP NOT NULL
);


DROP TABLE IF EXISTS comments;
CREATE TABLE comments (
  Id INT NOT NULL PRIMARY KEY,
  PostId INT NOT NULL REFERENCES posts(Id),
  UserId INT REFERENCES users(Id),
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
  PostId INT NOT NULL REFERENCES posts(Id),
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
  RelatedPostId INT NOT NULL REFERENCES posts(Id),
  PostId INT NOT NULL REFERENCES posts(Id),
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
  ParentId INTEGER REFERENCES posts(Id),
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
    UserId INT  REFERENCES users(Id),
    PostId INT NOT NULL REFERENCES posts(Id),
    VoteTypeId INT NOT NULL,
    BountyAmount INT ,
    CreationDate TIMESTAMP NOT NULL
);

END TRANSACTION;
