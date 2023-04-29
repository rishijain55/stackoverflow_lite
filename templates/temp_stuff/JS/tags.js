//top 20 tags with the most number of questions - fetched from backend
tags = [{
    TagName : "compiler",
    Id : 1,
    Count : 1,
}]

//get top 20 tags after creationdate 
fetchtags = [{
    TagName: "cplusplus",
    Id: 2,
    Count: 100
}]

fetchBtn = document.getElementById('fetch');
monitorElement = document.getElementById('monitor');
console.log(monitorElement);

fetchBtn.addEventListener('click', function(event) {
    event.preventDefault();

    // read the mm/yyyy from input name="creation-date"
    const input = document.getElementsByName('creation-date')[0];
    const inputValue = input.value;
    [dd, mm, yy] = inputValue.split('/');
    console.log(dd, mm, yy);

    //Fetch the growth rates from the backend to growthRates
})

//create table header rows
const table = document.createElement('table');
const headerRow = document.createElement('tr');
const nameHeader = document.createElement('th');
nameHeader.textContent = 'TagName';
const idHeader = document.createElement('th');
idHeader.textContent = 'Id';
const countHeader = document.createElement('th');
countHeader.textContent = 'Count';
headerRow.appendChild(nameHeader);
headerRow.appendChild(idHeader);
headerRow.appendChild(countHeader);
table.appendChild(headerRow);


//create table body rows
fetchtags.forEach(fectchtag => {
    const row = document.createElement('tr');
    const nameCell = document.createElement('td');
    nameCell.textContent = fectchtag.TagName;
    const idCell = document.createElement('td');
    idCell.textContent = fectchtag.Id;
    const countCell = document.createElement('td');
    countCell.textContent = fectchtag.Count;
    row.appendChild(nameCell);
    row.appendChild(idCell);
    row.appendChild(countCell);
    table.appendChild(row);
  });


monitorElement.appendChild(table);


deletelement = document.getElementById('delete')
// console.log
//create table header rows
const table2 = document.createElement('table');
const headerRow2 = document.createElement('tr');
const nameHeader2 = document.createElement('th');
nameHeader2.textContent = 'TagName';
const idHeader2 = document.createElement('th');
idHeader2.textContent = 'Id';
const countHeader2 = document.createElement('th');
countHeader2.textContent = 'Count';
headerRow2.appendChild(nameHeader2);
headerRow2.appendChild(idHeader2);
headerRow2.appendChild(countHeader2);
table2.appendChild(headerRow2);


//create table body rows
tags.forEach(tag => {
    const row2 = document.createElement('tr');
    const nameCell2 = document.createElement('td');
    nameCell2.textContent = tag.TagName;
    const idCell2 = document.createElement('td');
    idCell2.textContent = tag.Id;
    const countCell2 = document.createElement('td');
    countCell2.textContent = tag.Count;
    row2.appendChild(nameCell2);
    row2.appendChild(idCell2);
    row2.appendChild(countCell2);
    table2.appendChild(row2);
  });


deletelement.appendChild(table2);


