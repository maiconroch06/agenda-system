// pega um elemento usando um seletor CSS.
const user_form_login = document.querySelector('#form-login');

//document.querySelector('#user-email');  // id
//document.querySelector('.campo__erro'); // classe
//document.querySelector('input');         // elemento HTML

function validateUserLogin(email, senha){
    

    if (email === '' || senha === ''){
        return'ATENÇÃO, e-mail e senha devem ser preenchidos!';
    }

    return null;

}

//Validação para o USUARIO E LOGIN
user_form_login.addEventListener('submit', function(event){
    
        const email = document.querySelector("#client-email").value; //sem o # oiu o . significa elemento
        const senha = document.querySelector("#client-password").value;
        const message = document.querySelector("#validation-menssage");//significa o elemento p
        const div = document.querySelector('#div-validation-message');
        message.textContent = '';
        
        const errors = [];

        const erro_1 = validateUserLogin(email,senha);
        errors.push(...validateEmail(email));
        
        if (erro_1) {
            errors.push(erro_1); 
        }
      
             

        if (errors.length > 0){
            event.preventDefault(); //mecanismo que intercepta o envio para o action antes de chegar ao Flask.
            errors.forEach(
                function(erro){
                    message.innerHTML += erro + '</br>';
                }
            );
            div.classList.remove('hidden'); // Remove a ocultação do elemento
        }

});


//responsavel por verificar a formatação do email
function validateEmail(email) {

    const errors = [];

    if (email.length <= 4) {
        errors.push('ATENÇÃO, o e-mail deve possuir mais de 4 caracteres');
    }

    if (!email.includes('@')) { //verifica se existe @
        errors.push('ATENÇÃO, o e-mail deve possuir @');
    }

    if (!email.includes('.')) {
        errors.push('ATENÇÃO, o e-mail deve possuir .');
    }

    if (email.endsWith('.')) {//verifica se o texto termina com .
        errors.push('ATENÇÃO, o e-mail não pode terminar com .');
    }

    return errors;
}





