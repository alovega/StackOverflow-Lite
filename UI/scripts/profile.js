function showQuestionCards(divId){
    if (divId == 'userQuestions') {
        document.getElementById('UserQuestions').style.display = 'block';
        document.getElementById('UserAnswers').style.display = 'none';
    }
    if (divId == 'userAnswers') {
        document.getElementById('userQuestions').style.display = 'none';
        document.getElementById('userAnswers').style.display = 'block';
    }
}

function showWebStatistics(){
       document.getElementsByClassName("web-statistics")[0].style.display = 'table';
}

function showAnswerForm(){
       document.getElementsByClassName('Question-form')[0].style.display = 'block';
}
function showAnswerForm2(){
       document.getElementsByClassName('Question-form')[1].style.display = 'block';
}
function showAnswerForm3(){
       document.getElementsByClassName('Question-form')[2].style.display = 'block';
}

function closeForm(){
        document.getElementsByClassName('Question-form')[0].style.display = 'none';
 }
 function closeForm2(){
        document.getElementsByClassName('Question-form')[1].style.display = 'none';
 }
 function closeForm3(){
        document.getElementsByClassName('Question-form')[2].style.display = 'none';
 }
 function ShowAnswerList(){
        document.getElementsByClassName('answerList')[0].style.display = 'block';
 }

 function ShowMostAnswered(){
        document.getElementById('')
 }