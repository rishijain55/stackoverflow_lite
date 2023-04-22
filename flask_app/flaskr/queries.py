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
        )
        
        PostIds AS (
        SELECT AllVotes.Id, users.Reputation/10 + AllVotes.upvoteCount*10 + AllVotes.downvoteCount*10 + AllVotes.Score*50 AS totalScore
        FROM AllVotes, users
        WHERE AllVotes.OwnerUserId = users.Id
        ORDER BY totalScore DESC
        LIMIT 100;
        )

        SELECT * FROM posts WHERE Id IN (SELECT Id FROM PostIds);
    '''
}