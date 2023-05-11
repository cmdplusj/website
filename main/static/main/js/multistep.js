var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab
document.getElementById("id_field_of_design").selectedIndex = -1;// Initially no field of design is selected
// Initially no question is selected
if(document.getElementById("id_question1")!=undefined){
  document.getElementById("id_question1").selectedIndex = -1;
}
if(document.getElementById("id_question2")!=undefined){
  document.getElementById("id_question2").selectedIndex = -1;
}
if(document.getElementById("id_question3")!=undefined){
  document.getElementById("id_question3").selectedIndex = -1;
}

function showTab(n) {
  // This function will display the specified tab of the form...
  var x = document.getElementsByClassName("tab");
  x[n].style.display = "block";
  //... and fix the Previous/Next buttons:
  if (n == 0) {
    document.getElementById("prevBtn").style.display = "none";
  } else {
    document.getElementById("prevBtn").style.display = "inline";
  }
  if (n == (x.length - 1)) {
    document.getElementById("nextBtn").innerHTML = "Submit";
  } else {
    document.getElementById("nextBtn").innerHTML = "Next";
  }
  //... and run a function that will display the correct step indicator:
  fixStepIndicator(n)
}

function nextPrev(n) {
  // This function will figure out which tab to display
  var x = document.getElementsByClassName("tab");
  // Exit the function if any field in the current tab is invalid:
  if (n == 1 && !validateForm()) return false;
  // Hide the current tab:
  x[currentTab].style.display = "none";
  // Increase or decrease the current tab by 1:
  currentTab = currentTab + n;
  // if you have reached the end of the form...
  if (currentTab >= x.length) {
    // ... the form gets submitted:
    document.getElementById("regForm").submit();
    return false;
  }
  // Otherwise, display the correct tab:
  showTab(currentTab);
}

function validateForm() {
  // This function deals with validation of the form fields
  var x, y, i, valid = true;
  x = document.getElementsByClassName("tab");
  y = x[currentTab].getElementsByTagName("input");
  ta = x[currentTab].getElementsByTagName("textarea");
  // A loop that checks every input field in the current tab:
  for (i = 0; i < y.length; i++) {
    // If a field is empty...
    if(y[i].id=="id_email"){
      var reEmail = /^(?:[\w\!\#\$\%\&\'\*\+\-\/\=\?\^\`\{\|\}\~]+\.)*[\w\!\#\$\%\&\'\*\+\-\/\=\?\^\`\{\|\}\~]+@(?:(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-](?!\.)){0,61}[a-zA-Z0-9]?\.)+[a-zA-Z0-9](?:[a-zA-Z0-9\-](?!$)){0,61}[a-zA-Z0-9]?)|(?:\[(?:(?:[01]?\d{1,2}|2[0-4]\d|25[0-5])\.){3}(?:[01]?\d{1,2}|2[0-4]\d|25[0-5])\]))$/;
      if(!y[i].value.match(reEmail)) {
        y[i].className += " invalid";
        valid = false;
        var email_error = document.getElementById("email_errors");
        email_error.style.display = "block";
        console.log("wrong email");
      }
      else{
        var email_error = document.getElementById("email_errors");
        email_error.style.display = "none";
        y[i].className -= " invalid";
      }
      console.log("correct email");
    }
    else if(y[i].id=="id_password1"){
      var password1 = document.getElementById("id_password1");
      var password2 = document.getElementById("id_password2");
      var password_error_1 = document.getElementById("password_errors_1");
      password_error_1.style.display = "none";
      var password_error_2 = document.getElementById("password_errors_2");
      password_error_2.style.display = "none";
      if(password1.value.length<8){
        y[i].className += " invalid";
        valid = false;
        var password_error_1 = document.getElementById("password_errors_1");
        password_error_1.style.display = "block";
        console.log("length of password is less than 8");
      }
      else if(password1.value!=password2.value){
        y[i].className += " invalid";
        valid = false;
        var password_error_2 = document.getElementById("password_errors_2");
        password_error_2.style.display = "block";
        console.log("Passwords do not match");
      }
      else{
        y[i].className -= " invalid";
      }
    }
    else if(y[i].id!="id_social_url"){
      if (y[i].value == "") {
        // add an "invalid" class to the field:
        y[i].className += " invalid";
        // and set the current valid status to false
        valid = false;
      }
      else{
        y[i].className -= " invalid";
      }
    }
  }

  for (i = 0; i < ta.length; i++) {
    if (ta[i].value == "") {
      // add an "invalid" class to the field:
      ta[i].className += " invalid";
      // and set the current valid status to false
      valid = false;
    }
    else{
      ta[i].className -= " invalid";
    }
  }


  if(currentTab == 1){
    var field_of_design = document.getElementById("id_field_of_design");
    if(field_of_design.selectedIndex == -1){
      field_of_design.className += " invalid";
      valid = false;
    }
    else{
      field_of_design.className -= " invalid";
    }
  }
  else if(currentTab == 2){
    var question1 = document.getElementById("id_question1");
    if(question1 != undefined){
      if(question1.selectedIndex == -1){
        question1.className += " invalid";
        valid = false;
      }
      else{
        question1.className -= " invalid";
      }
    }
    var question2 = document.getElementById("id_question2");
    if(question2 != undefined){
      if(question2.selectedIndex == -1){
        question2.className += " invalid";
        valid = false;
      }
      else{
        question2.className -= " invalid";
      }
    }
    if(question3 != undefined){
      var question3 = document.getElementById("id_question3");
      if(question3.selectedIndex == -1){
        question3.className += " invalid";
        valid = false;
      }
      else{
        question3.className -= " invalid";
      }
    }
  }

  // If the valid status is true, mark the step as finished and valid:
  if (valid) {
    document.getElementsByClassName("step")[currentTab].className += " finish";
  }
  return valid; // return the valid status
}

function fixStepIndicator(n) {
  // This function removes the "active" class of all steps...
  var i, x = document.getElementsByClassName("step");
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(" active", "");
  }
  //... and adds the "active" class on the current step:
  x[n].className += " active";
}

var limit = 4;
$('input.limit-checkbox').on('change', function(evt) {
   if($("input[name='tag']:checked").length > limit) {
       this.checked = false;
       var tag_errors = document.getElementById("tag_errors");
       tag_errors.style.display = "block";
   }
   else{
    var tag_errors = document.getElementById("tag_errors");
    tag_errors.style.display = "none";
   }
});

$("#id_question1").on('change', function(evt) {
  var selectedQuestionStr1 = $(this).children("option:selected").val();
  var selectedQuestion1 = parseInt(selectedQuestionStr1.slice(1));
  var selectedQuestionStr2 = $("#id_question2").children("option:selected").val();
  var selectedQuestionStr3 = $("#id_question3").children("option:selected").val();
  console.log(selectedQuestionStr2);
  console.log(selectedQuestion1);
  var length_q2 = $('#id_question2 > option').length;
  console.log(length_q2);
  var i;
  for (i = 0; i < length_q2; i++) {
    document.getElementById("id_question2").options[i].disabled = false;
    document.getElementById("id_question3").options[i].disabled = false;
  }
  if(selectedQuestionStr2 != undefined){
    var selectedQuestion2 = parseInt(selectedQuestionStr2.slice(1));
    document.getElementById("id_question1").options[selectedQuestion2-1].disabled = true;
    document.getElementById("id_question3").options[selectedQuestion2-1].disabled = true;
  }
  if(selectedQuestionStr3 != undefined){
    var selectedQuestion3 = parseInt(selectedQuestionStr3.slice(1));
    document.getElementById("id_question1").options[selectedQuestion3-1].disabled = true;
    document.getElementById("id_question2").options[selectedQuestion3-1].disabled = true;
  }
  document.getElementById("id_question2").options[selectedQuestion1-1].disabled = true;
  document.getElementById("id_question3").options[selectedQuestion1-1].disabled = true;
});

$("#id_question2").on('change', function(evt) {
  var selectedQuestionStr = $(this).children("option:selected").val();
  var selectedQuestion = parseInt(selectedQuestionStr.slice(1));
  var selectedQuestionStr1 = $("#id_question1").children("option:selected").val();
  var selectedQuestionStr3 = $("#id_question3").children("option:selected").val();

  console.log(selectedQuestion);
  var length_q2 = $('#id_question2 > option').length;
  console.log(length_q2);
  var i;
  for (i = 0; i < length_q2; i++) {
    document.getElementById("id_question1").options[i].disabled = false;
    document.getElementById("id_question3").options[i].disabled = false;
  }
  if(selectedQuestionStr1 != undefined){
    var selectedQuestion1 = parseInt(selectedQuestionStr1.slice(1));
    document.getElementById("id_question2").options[selectedQuestion1-1].disabled = true;
    document.getElementById("id_question3").options[selectedQuestion1-1].disabled = true;
  }
  if(selectedQuestionStr3 != undefined){
    var selectedQuestion3 = parseInt(selectedQuestionStr3.slice(1));
    document.getElementById("id_question1").options[selectedQuestion3-1].disabled = true;
    document.getElementById("id_question2").options[selectedQuestion3-1].disabled = true;
  }
  document.getElementById("id_question1").options[selectedQuestion-1].disabled = true;
  document.getElementById("id_question3").options[selectedQuestion-1].disabled = true;
});

$("#id_question3").on('change', function(evt) {
  var selectedQuestionStr = $(this).children("option:selected").val();
  var selectedQuestion = parseInt(selectedQuestionStr.slice(1));
  var selectedQuestionStr1 = $("#id_question1").children("option:selected").val();
  var selectedQuestionStr2 = $("#id_question2").children("option:selected").val();

  console.log(selectedQuestion);
  var length_q2 = $('#id_question2 > option').length;
  console.log(length_q2);
  var i;
  for (i = 0; i < length_q2; i++) {
    document.getElementById("id_question2").options[i].disabled = false;
    document.getElementById("id_question1").options[i].disabled = false;
  }
  if(selectedQuestionStr1 != undefined){
    var selectedQuestion1 = parseInt(selectedQuestionStr1.slice(1));
    document.getElementById("id_question2").options[selectedQuestion1-1].disabled = true;
    document.getElementById("id_question3").options[selectedQuestion1-1].disabled = true;
  }
  if(selectedQuestionStr2 != undefined){
    var selectedQuestion2 = parseInt(selectedQuestionStr2.slice(1));
    document.getElementById("id_question1").options[selectedQuestion2-1].disabled = true;
    document.getElementById("id_question3").options[selectedQuestion2-1].disabled = true;
  }
  document.getElementById("id_question2").options[selectedQuestion-1].disabled = true;
  document.getElementById("id_question1").options[selectedQuestion-1].disabled = true;
});