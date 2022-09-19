const openModalButtons = document.querySelectorAll('[data-modal-target]')
const closeModalButtons =document.querySelectorAll('[data-close-button]')
const overlay =document.getElementById('overlay')

openModalButtons.forEach(button => {
    button.addEventListener('click',() =>{
        const modal = document.querySelector(button.dataset.modalTarget)
        openModal(modal)
    })
})

closeModalButtons.forEach(button => {
    button.addEventListener('click',() =>{
        const  modal = button.closest('.modal')
        closeModal(modal)
    })
})



function openModal(modal){
    if(modal == null) return
    modal.classList.add('active')
    overlay.classList.add('active')
}

function closeModal(modal){
    if(modal == null) return
    modal.classList.remove('active')
    overlay.classList.remove('active')
}










const checkUserName = () => {
    const Full_name = document.getElementById("fullname").value;
    if (Full_name == "" ) {
      document.getElementById("name_error").innerHTML += "<p> name should not be blank </p>";
      setTimeout(() => {
        document.getElementById("name_error").innerHTML = "";
      }, 2000);
      return false;
    }
  
     else if ( username.length >= 15 ) {
       document.getElementById("name_error").innerHTML += "<p> username exceeds 15 characters </p>";
       console.log("chkk");
  
       setTimeout(() => {
         document.getElementById("name_error").innerHTML = "";
       }, 2000);
       return false;
     }
  
     else  if ( username.length < 8) {
        document.getElementById("name_error").innerHTML +=
          "<p> username too short . :) </p>";
        setTimeout(() => {
          document.getElementById("name_error").innerHTML = "";
        }, 2000);
        return false;
      }
  
    return true;
  };
  
  
  const checkEmail = () => {
    const email = document.getElementById("emailtext").value;
    if (!email.includes("@", 1) || /^[\!#$%&*_+|/>,<;{}[]()]*$/.test(email)) {
      document.getElementById("email_error").innerHTML += "<p>Wrong email id</p>";
      setTimeout(() => {
        document.getElementById("email_error").innerHTML = "";
      }, 2000);
      return false;
    }
    return true;
  };
  
  
  const checkPassword = () => {
    const password = document.getElementById("passwordtext").value;
    if (!/[0-9 a-z A-Z]+/.test(password)) {
      document.getElementById("password_error").innerHTML +=
        "<p>Wrong password</p>";
  
      setTimeout(() => {
        document.getElementById("password_error").innerHTML = "";
      }, 2000);
      return false;
    } 
    
    
    else if (password.length < 8) {
      document.getElementById("password_error").innerHTML += "<p>Too short</p>";
      setTimeout(() => {
        document.getElementById("password_error").innerHTML = "";
      }, 2000);
      return false;
    } 
  
  
  
    else if (!/[!@#$%^&*()_]+/.test(password)) {
      document.getElementById("password_error").innerHTML +=
        "<p>No special symbols included add !@#$%^&*()_</p>";
      setTimeout(() => {
        document.getElementById("password_error").innerHTML = "";
      }, 2000);
      return false;
    } 
    return true;
  };
  
  document.querySelector(".submit").addEventListener("click", (e) => {
    e.preventDefault();
    const validUserName = checkUserName();
    const validEmail = checkEmail();
    const validPassword = checkPassword();
    if (validUserName && validEmail && validPassword)
      console.log("Everything is Valid :)))");
      
  });
  
  
  