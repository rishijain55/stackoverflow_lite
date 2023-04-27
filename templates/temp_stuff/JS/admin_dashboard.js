growthRates = [{
    year: 2020,
    month: 1,
    users: 100
}]

fetchBtn = document.getElementById('fetch');
monitorElement = document.getElementById('monitor');
console.log(monitorElement);
fetchBtn.addEventListener('click', function(event) {
    event.preventDefault();

    // read the mm/yyyy from input name="creation-date"
    const input = document.getElementsByName('creation-date')[0];
    const inputValue = input.value;
    [mm, yy] = inputValue.split('/');
    console.log(mm, yy);

    //Fetch the growth rates from the backend to growthRates
})

const table = document.createElement('table');

// Create table header row
const headerRow = document.createElement('tr');
const yearHeader = document.createElement('th');
yearHeader.textContent = 'Year';
const monthHeader = document.createElement('th');
monthHeader.textContent = 'Month';
const usersHeader = document.createElement('th');
usersHeader.textContent = 'Number of Users';
headerRow.appendChild(yearHeader);
headerRow.appendChild(monthHeader);
headerRow.appendChild(usersHeader);
table.appendChild(headerRow);

// Create table body rows
growthRates.forEach(growthRate => {
  const row = document.createElement('tr');
  const yearCell = document.createElement('td');
  yearCell.textContent = growthRate.year;
  const monthCell = document.createElement('td');
  monthCell.textContent = growthRate.month;
  const usersCell = document.createElement('td');
  usersCell.textContent = growthRate.users;
  row.appendChild(yearCell);
  row.appendChild(monthCell);
  row.appendChild(usersCell);
  table.appendChild(row);
});

monitorElement.appendChild(table);

form = document.getElementById('delete');

form.addEventListener('submit', (event) => {
    event.preventDefault();
    const scoreInput = document.getElementsByName('score')[0];
    const score = scoreInput.value;
    console.log(score);

})