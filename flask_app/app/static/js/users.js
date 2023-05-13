//top 50 users with max reputation - backend 
users_repu = [{
    DisplayName : "john",
    Id : 1,
    Reputation : 100,
}]


//admins of our platform
admins = [{
    DisplayName : "sam",
    Id : 2,
}]

//new user recommendations
users_recom = [{
    DisplayName : "ben",
    Id : 1,
}]

reputationelement = document.getElementById('repu');

//create table header rows
const table1 = document.createElement('table');
const headerRow1 = document.createElement('tr');
const nameHeader1 = document.createElement('th');
nameHeader1.textContent = 'DisplayName';
const idHeader1 = document.createElement('th');
idHeader1.textContent = 'Id';
const repuheader1 = document.createElement('th');
repuheader1.textContent = 'Reputation';
headerRow1.appendChild(nameHeader1);
headerRow1.appendChild(idHeader1);
headerRow1.appendChild(repuheader1);
table1.appendChild(headerRow1);


//create table body rows
users_repu.forEach(repuser => {
    const row1 = document.createElement('tr');
    const nameCell1 = document.createElement('td');
    nameCell1.textContent = repuser.DisplayName;
    const idCell1 = document.createElement('td');
    idCell1.textContent = repuser.Id;
    const countCell1 = document.createElement('td');
    countCell1.textContent = repuser.Reputation;
    row1.appendChild(nameCell1);
    row1.appendChild(idCell1);
    row1.appendChild(countCell1);
    table1.appendChild(row1);
  });


reputationelement.appendChild(table1);


adminelement = document.getElementById('admi');

//create table header rows
const table2 = document.createElement('table');
const headerRow2 = document.createElement('tr');
const nameHeader2 = document.createElement('th');
nameHeader2.textContent = 'DisplayName';
const idHeader2 = document.createElement('th');
idHeader2.textContent = 'Id'
headerRow2.appendChild(nameHeader2);
headerRow2.appendChild(idHeader2);
table2.appendChild(headerRow2);


//create table body rows
admins.forEach(adminnn => {
    const row2 = document.createElement('tr');
    const nameCell2 = document.createElement('td');
    nameCell2.textContent = adminnn.DisplayName;
    const idCell2 = document.createElement('td');
    idCell2.textContent = adminnn.Id;
    row2.appendChild(nameCell2);
    row2.appendChild(idCell2);
    table2.appendChild(row2);
  });

  adminelement.appendChild(table2);


  recomelement = document.getElementById('recom');

  //create table header rows
  const table3 = document.createElement('table');
  const headerRow3 = document.createElement('tr');
  const nameHeader3 = document.createElement('th');
  nameHeader3.textContent = 'DisplayName';
  const idHeader3 = document.createElement('th');
  idHeader3.textContent = 'Id'
  headerRow3.appendChild(nameHeader3);
  headerRow3.appendChild(idHeader3);
  table3.appendChild(headerRow3);
  
  
  //create table body rows
  users_recom.forEach(recomm => {
      const row3 = document.createElement('tr');
      const nameCell3 = document.createElement('td');
      nameCell3.textContent = recomm.DisplayName;
      const idCell3 = document.createElement('td');
      idCell3.textContent = recomm.Id;
      row3.appendChild(nameCell3);
      row3.appendChild(idCell3);
      table3.appendChild(row3);
    });
  
    recomelement.appendChild(table3);

