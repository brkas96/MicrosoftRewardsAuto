# MicrosoftRewardsAuto

:rocket: Support this project: [![Patrocine este projeto](https://img.shields.io/badge/-Sponsor-fafbfc?logo=GitHub%20Sponsors)](https://github.com/sponsors/brkas96)

### :white_check_mark: ABOUT:

This is a **Python** automation project that uses **Selenium** to automatically complete missions on **Microsoft Rewards**. 
The script interacts with the Microsoft Rewards website, logging in to the account and performing tasks such as 
claiming points, completing daily sets, and other available missions. This automation helps streamline the process 
and ensure consistent activity for earning rewards without manual intervention.

### :white_check_mark: HOW TO USE:

The compiled program can be found in the **dist folder** of this project. However, if you want to compile it yourself, 
create a virtual environment, install the dependencies defined in the requirements.txt, and compile it using 
PyInstaller with the main.spec file provided in this project.

- Rename the file "pass_exemple.json" to just "pass.json".
- Add your Microsoft account credentials to it (your email and password).
- The pass.json must be in the same directory as the program's executable.
- Open the Windows Task Scheduler and configure the program to start according to your preferences.
- Arguments in Windows Task Scheduler (Exemple):
    - Program/Script: `"C:\Users\USERNAME\OneDrive\Documents\Compiled Python Programs\Microsoft Rewards Auto\Microsoft Rewards Auto.exe"`
    - Add arguments (optional): ``
    - Start in (optional): `C:\Users\USERNAME\OneDrive\Documents\Compiled Python Programs\Microsoft Rewards Auto`


### COMO USAR (PT-BR):

- Primeiro, renomeie o arquivo "pass_exemple.json" para apenas "pass.json"
- Coloque as credenciais da sua conta Microsoft nele. (Seu email e senha)
- A pasta "audios" já está inclusa no compilado exe.
- Abra o Agendador de Tarefas do Windows e configure o programa para iniciar de acordo com suas preferencias
- Argumentos no Agendador de Tarefas do Windows (Exemplo):
    - Programa/Script: "C:\Users\USERNAME\OneDrive\Documentos\Programas Python Compilados\Microsoft Rewards Auto\Microsoft Rewards Auto.exe"
    - Adicione argumentos (opcional): ""
    - Iniciar em (opcional): C:\Users\USERNAME\OneDrive\Documentos\Programas Python Compilados\Microsoft Rewards Auto

### Problemas para resolver
Vez ou outra, pode aparecer a tela para confirmar minha infomações de segurança durante o login, perguntando se eu quero
mudar alguma coisa. Implementei a função "confirmar_informacoes()" para tentar clicar no botão e processeguir com o login
porém ainda não funcionou. Vou ter que aguardar essa tela aparecer novamente para testar alguma forma que dê certo.
