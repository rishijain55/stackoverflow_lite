//Fetch this through backend
interestingQuestions = [{
    Question : "Check if Two Arrays Sorted in Decreasing and Increasing Order Satisfy a Condition",
    id : 1,
    votes : 1,
    tags : ["arrays", "permutation"],
    author : "Avv",
    numAnswers : 2,
    accepted : true,
},{
    Question : "Check if Two Arrays Sorted in Decreasing and Increasing Order Satisfy a Condition",
    id : 1,
    votes : 1,
    tags : ["arrays", "permutation"],
    author : "Avv",
    numAnswers : 2,
    accepted : true,
}]

// interestingQuestions.push(interestingQuestions[0])
// interestingQuestions.push(interestingQuestions[0])
// interestingQuestions.push(interestingQuestions[0])
// interestingQuestions.push(interestingQuestions[0])
// interestingQuestions.push(interestingQuestions[0])
// interestingQuestions.push(interestingQuestions[0])
// interestingQuestions.push(interestingQuestions[0])


listqeu = document.getElementById("interesting-questions");
// traverse through interestingQuestions
interestingQuestions.forEach(q => {
    // Create the first div element with the question title, author, and tags
  const div1 = document.createElement("div");
  div1.className = "question-info";
  
  const title = document.createElement("a");
  title.className = "cd-faq-trigger"
  title.innerText = q.Question;
  div1.appendChild(title);
  
  const author = document.createElement("p");
  author.innerText = `Author: ${q.author}`;
  div1.appendChild(author);
  
  const tags = document.createElement("div");
  tags.className = "tags";
  tags.innerText = `Tags: ${q.tags.join(", ")}`;
  div1.appendChild(tags);
  
  // Create the second div element with the remaining question values
  const div2 = document.createElement("div");
  div2.className = "question-details";
  
  const votes = document.createElement("p");
  votes.innerText = `Votes: ${q.votes}`;
  div2.appendChild(votes);
  
  const numAnswers = document.createElement("p");
  numAnswers.innerText = `Answers: ${q.numAnswers}`;
  div2.appendChild(numAnswers);
  
  const accepted = document.createElement("p");
  accepted.innerText = `Accepted: ${q.accepted}`;
  div2.appendChild(accepted);
  
  // Add the two div elements to a new list item element
  const li = document.createElement("li");
  li.appendChild(div1);
  li.appendChild(div2);
  
  // Add the new list item element to the unordered list
  listqeu.querySelector("ul").appendChild(li);
});

//This is the leaderboard fetch from the backend
leaderboard = [{
    DisplayName : "Temp-name 1",
    Id : 1,
    totalScore : 230
}]

leaderboardTag = document.getElementById("leaderboard")
leaderboard.forEach(profile => {
    const nameTag = document.createElement("a")
    nameTag.innerText = profile.DisplayName
    nameTag.setAttribute("href", "#0")

    const scoreTag = document.createElement("div")
    scoreTag.innerText = profile.totalScore

    const div = document.createElement("div")

    div.appendChild(nameTag);
    div.appendChild(scoreTag)

    leaderboardTag.appendChild(div);
})


if(login){

}