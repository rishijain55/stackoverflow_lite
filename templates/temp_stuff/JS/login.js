const loginForm = document.getElementById('login-form');

if(loginForm != null)
{  
  loginForm.addEventListener('submit', function(event) {
    event.preventDefault();
    
    const usernameInput = document.getElementById('login-form').elements.namedItem('username');
    const usernameValue = usernameInput.value;
    
    console.log(usernameValue);

    const usernamePassword = document.getElementById('login-form').elements.namedItem('password');
    const passwordValue = usernamePassword.value;

    console.log(passwordValue);
    
    // You can now use the usernameValue variable to do something with the
  })
}

const signupForm = document.getElementById('signup-form');

if(signupForm != null)
{
  signupForm.addEventListener('submit', function(event) {
  event.preventDefault();

  const emailInput = document.getElementById('signup-form').elements.namedItem('email');
  const emailValue = emailInput.value;

  console.log(emailValue);

  const usernameInput = document.getElementById('signup-form').elements.namedItem('username');
  const usernameValue = usernameInput.value;

  console.log(usernameValue);

  const usernamePassword1 = document.getElementById('signup-form').elements.namedItem('password1');
  const passwordValue1 = usernamePassword1.value;

  const usernamePassword2 = document.getElementById('signup-form').elements.namedItem('password2');
  const passwordValue2 = usernamePassword2.value;

  console.log(passwordValue1);
  console.log(passwordValue2);

  if(passwordValue1 != passwordValue2){
    const errorMessage = document.getElementById('error-message');
    errorMessage.textContent = 'Password do not match';
  }
  })
}

const adminloginForm = document.getElementById('admin-login');

if(adminloginForm != null)
{  
  adminloginForm.addEventListener('submit', function(event) {
    event.preventDefault();
    
    const usernameInput = document.getElementById('admin-login').elements.namedItem('username');
    const usernameValue = usernameInput.value;
    
    console.log(usernameValue);

    const usernamePassword = document.getElementById('admin-login').elements.namedItem('password');
    const passwordValue = usernamePassword.value;

    console.log(passwordValue);
    
    // You can now use the usernameValue variable to do something with the
  })
}