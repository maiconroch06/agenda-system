# 1. Instalação do ambiente Virtual - LINUX

> 1. sudo apt update
> 2. sudo apt install python3-venv -y
 >>   1. esse comando instala o pacote necessário para criar ambientes virtuais do Python
>3. python3 -m venv .venv
>4. source .venv/bin/activate
>5. deactivate

# 2. Instalação do ambiente Virtual - WINDOWS

1. python --version
2. python -m venv .venv
3. .venv\Scripts\Activate.ps1
4. Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    1. O comando acima deve ser utilizado quando PowerShell bloquear o script
5. .venv\Scripts\Activate.ps1


## 2. 1. Verificações sobre a instalação do python 
1. python --version
2. where.exe python 
    1. SAÍDA DO COMANDO{.venv\Scripts\python.exe}
3. python -m pip install --upgrade pip
4. pip install flask

## 3. COMANDOS FUTUROS
> Se quiser que outros dispositivos da sua rede possam acessar a API
> flask --app main run --host=0.0.0.0 --port=5000


## 4. COMANDOS PARA ACESSAR ARQUIVOS

>img src="{{ url_for('static', filename='img/logo.png') }}"
>  
>link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">;
>
>script src="{{ url_for('static', filename='js/script.js') }}"
>
>As fontes são englobadas aqui!

## 5. Diagramas
## 6. Casos de uso

