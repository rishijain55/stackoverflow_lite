//This will get the question from backend before loading
question = {
    title : "How to count this operation for (int interval = n/2; interval > 0; interval /= 2) using counting primitive operation?",
    body : "I was confused how to label this for (int interval = n/2; interval > 0; interval /= 2)  with counting operation and estimating this operation so that I can get that exact Running time of this shell short algorithm",
    id : 1,  
    upvote : 1,
    downvote : 1,
} 

//This are the answers to the questions with the id above
answers = [{
    id : 1,
    text : "Assuming that the body of the main loop takes f(n) operations, the total operation count will be (for n an exact power of 2)",
    upvote : 1,
    downvote : 1,
}]

related = [{
    Question : "Check if Two Arrays Sorted in Decreasing and Increasing Order Satisfy a Condition",
    id : 2,
    votes : 1,
    tags : ["arrays", "permutation"],
    author : "Avv",
    numAnswers : 2,
    accepted : true,
}]

mainDiv = document.getElementById("main");

div1 = document.createElement("div");
div2 = document.createElement("div");

div1.innerHTML = `<h2>${question.title}</h2>`

divQbody = document.createElement("div");
divQbody.innerHTML = `<p>${question.body}</p>`
btnUpvote = document.createElement("button");
btnUpvote.innerHTML = `<i class="fas fa-arrow-up">${question.upvote}</i>`
btnDownvote = document.createElement("button");
btnDownvote.innerHTML = `<i class="fas fa-arrow-down">${question.downvote}</i>`

divQbody.appendChild(btnUpvote);
divQbody.appendChild(btnDownvote);
div1.appendChild(divQbody);

div1.innerHTML += `<h2>Answers</h2>`
answers.forEach(answer => {
    divAtext = document.createElement("div");
    divAtext.innerHTML = `<p>${answer.text}</p>`
    btnUpvoteAns = document.createElement("button");
    btnUpvoteAns.innerHTML = `<i class="fas fa-arrow-up">${answer.upvote}</i>`
    btnDownvoteAns = document.createElement("button");
    btnDownvoteAns.innerHTML = `<i class="fas fa-arrow-down">${answer.downvote}</i>`
    divAtext.appendChild(btnUpvoteAns);
    divAtext.appendChild(btnDownvoteAns);

    div1.appendChild(divAtext);
});

div2.innerHTML = `<h2>Related Questions</h2>`

related.forEach(q => {
    // Create the first div element with the question title, author, and tags
    const divR = document.createElement("div");
    divR.className = "question-info";
    
    const title = document.createElement("a");
    title.className = "cd-faq-trigger"
    title.innerText = q.Question;
    divR.appendChild(title);

    const author = document.createElement("p");
    author.innerText = `Author: ${q.author}`;
    divR.appendChild(author);

    const tags = document.createElement("div");
    tags.className = "tags";

    tags.innerText = `Tags: ${q.tags.join(", ")}`;
    divR.appendChild(tags);

    // Create the second div element with the remaining question values
    const div2R = document.createElement("div");
    div2R.className = "question-details";

    const votes = document.createElement("p");
    votes.innerText = `Votes: ${q.votes}`;

    div2R.appendChild(votes);

    const numAnswers = document.createElement("p");
    numAnswers.innerText = `Answers: ${q.numAnswers}`;

    div2R.appendChild(numAnswers);
    div2.appendChild(divR);
})


mainDiv.appendChild(div1);
mainDiv.appendChild(div2);
