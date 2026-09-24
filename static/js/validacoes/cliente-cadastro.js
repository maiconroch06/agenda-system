const client_form_register = document.querySelector('#form-barber-shop');
const phone = document.querySelector('#client-telefone');
const password_confirm = document.querySelector('#client-conf-senha');
const password = document.querySelector('#cliente-senha');


password_confirm.addEventListener('input', function(){
    const password_status = validatePasswordConfirmPassword(password,password_confirm);

    if (password_status.length===0){
        password.classList.remove('border-red-500');
        password_confirm.classList.remove('border-red-500');
        document.querySelector('#div-validation-message').classList.add('hidden');
    }

});


phone.addEventListener('input',function(){//input é o evento que ocorre quando o conteúdo do campo é alterado
    // Pega o valor atual digitado no campo
    // replace - Remover tudo que não for número
    let  numeros = phone.value.replace(/\D/g, ''); 

    // Limita o telefone a no máximo 11 números
    if (numeros.length > 11) {
        numeros = numeros.slice(0, 11);// slice -> recortar/pegar uma parte" de uma string ou array.
    }

    // Se tiver até 2 números, mostra apenas o início do DDD
    if (numeros.length <= 2) {
        phone.value = '(' + numeros;
    }

    // Se tiver de 3 até 7 números
    else if (numeros.length <= 7) {
        phone.value =
            '(' + numeros.slice(0, 2) + ') ' +
            numeros.slice(2); //separa os números
    }

    // Se tiver mais de 7 números
    else {
        phone.value =
            '(' +
            numeros.slice(0, 2) + ') ' +
            numeros.slice(2, 7) + '-' +
            numeros.slice(7);
    }

});


client_form_register.addEventListener('submit',
    function(event){
            //atribui as variaaveis todos os campos do formulario
            const name = document.querySelector('#client-name');
            const email = document.querySelector('#client-email');
            
            
            
            // Pega a div onde vai ficar a mensagem;
            const div = document.querySelector('#div-validation-message');

            // pega o id onde vai ser apresentada a mensagem;
            const message = document.querySelector('#validation-menssage');
            message.textContent='';

            // Array onde ira receber todos os erros sobre as validações
            const errors = [];
            // O ... espalha o conteúdo do array,
            // Nas funções eu estou passando os elementos, os valores seram pegos nas funções.
            errors.push(...validarFieldNull(name, phone,email,password,password_confirm));
            errors.push(...validatePasswordConfirmPassword(password,password_confirm));
            errors.push(...validateEmail(email));
        
            if (errors.length > 0){
                event.preventDefault();
                errors.forEach(function(erro){
                    message.innerHTML += erro+'</br>';
                }
            );

                div.classList.remove('hidden'); // Remove a ocultação do elemento
            }
       

    }

);

//responsavel por verificar se algum campo é nulo
function validarFieldNull(name, phone,email,password,password_confirm){
    
    const error = [];
    
    if (name.value === '' || phone.value=== '' || email.value==='' || password.value === '' || password_confirm.value===''){
        error.push('ATENÇÃO, verifique se todos os campos estão preenchidos');
    
    }

    return error;

}

//Reponsável por validar o senha e confirmação da senha/
function validatePasswordConfirmPassword(password, password_confirm){
    const error = [];
    
    if (password.value !== password_confirm.value ){
        error.push('ATENÇÃO, senha e confirmar senha estão diferentes');
        password.classList.add('border-red-500');
        password_confirm.classList.add('border-red-500');
    }

    return error;
}

//responsavel por verificar a formatação do email
function validateEmail(email) {

    const errors = [];

    if (email.value.length <= 4) {
        errors.push('ATENÇÃO, o e-mail deve possuir mais de 4 caracteres');
    }

    if (!email.value.includes('@')) { //verifica se existe @
        errors.push('ATENÇÃO, o e-mail deve possuir @');
    }

    if (!email.value.includes('.')) {
        errors.push('ATENÇÃO, o e-mail deve possuir .');
    }

    if (email.value.endsWith('.')) {//verifica se o texto termina com .
        errors.push('ATENÇÃO, o e-mail não pode terminar com .');
    }

    return errors;
}