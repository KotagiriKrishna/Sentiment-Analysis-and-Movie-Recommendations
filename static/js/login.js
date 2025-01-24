document.addEventListener('DOMContentLoaded', function() {
    const signInForm = document.getElementById('signInForm');
    const signUpForm = document.getElementById('signUpForm');
    const registerLink = document.getElementById('registerLink');
    const signInLink = document.getElementById('signInLink');

    signInForm.style.display = 'block';
    signUpForm.style.display = 'none';

    registerLink.addEventListener('click', function(event) {
        event.preventDefault();
        signInForm.style.display = 'none';
        signUpForm.style.display = 'block';
    });

    signInLink.addEventListener('click', function(event) {
        event.preventDefault();
        signUpForm.style.display = 'none';
        signInForm.style.display = 'block';
    });
});

//data
document.getElementById("signUpForm").addEventListener("submit", function(event){
    event.preventDefault();
    var username = document.getElementById("signupEmail").value;
    var password = document.getElementById("signupPassword").value;
    
    fetch('/signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({username: username, password: password})
    })
    .then(response => response.json())
    .then(data => {
      alert(data.message);
      if (data.redirect_url){
        window.location.href = data.redirect_url;
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
  });
  
  document.getElementById("signInForm").addEventListener("submit", function(event){
    event.preventDefault();
    var username = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    
    fetch('/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({username: username, password: password})
    })
    .then(response => response.json())
    .then(data => {
      //alert(data.message);
      if (data.redirect_url){
        window.location.href = data.redirect_url;
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
  });
