# sinesp-bot

O sinesp-bot torna possível a consulta automatizada à base de dados do SINESP Cidadão sem a necessidade do preenchimento de captchas ou algum outro tipo de autenticação.

Esta é uma prova de conceito e oferece uma alternativa a bibliotecas como o [sinesp-client](https://github.com/victor-torres/sinesp-client/), que utilizam uma outra abordagem para obter acesso às APIs.


## O que é o SINESP

SINESP Cidadão é uma base de dados pública de veículos brasileiros. É muito útil para identificar carros ou motos roubados ou suspeitos.


## Informações disponíveis

Se um veículo com a placa especificada for encontrado, o servidor irá retornar as seguintes informações que serão repassadas através de um dicionário:

- return_code (código de retorno)
- return_message (mensagem de retorno)
- status_code (código do status)
- status_message (mensagem do status)
- chassis (chassi do veículo)
- model (modelo/versão)
- brand (marca/fabricante)
- color (cor/pintura)
- year (ano de fabricação)
- model_year (ano do modelo)
- plate (placa)
- date (data e hora da consulta)
- city (cidade)
- state (estado ou unidade federativa)


## Por que fazer um cliente do SINESP?

Não sabemos o porquê, mas o governo não mantém uma API pública para este serviço. A única maneira de acessar os dados é acessando o site do SINESP e respondendo a perguntas de verificação (captchas) para cada uma das requisições ou utilizando os aplicativos oficiais.

Permitir a automatização dessa tarefa possibilita que desenvolvedores de todo o país elaborem aplicações de retorno social importantíssimo, em sua maioria voltada para a segurança pública de ruas, condomínios, estabelecimentos comerciais, estacionamentos, escolas etc.


## O que nós fizemos

Felizmente as aplicações para Android e iOS permitem que a busca seja feita sem que seja preciso responder a nenhum teste captcha. Inicialmente, foi feita uma engenharia reversa no aplicativo por diversos membros da comunidade para que pudéssemos ter acesso a essas informações públicas sem que fosse preciso responder aos testes de captcha.

No entanto, a equipe do SINESP constantemente lança atualizações do aplicativo dificultando o acesso automatizado das informações e obfuscando a forma com a qual o acesso é feito.

Este repositório demonstra a utilização de uma técnica não invasiva utilizada principalmente em testes de QA. Usamos o SDK do Android e suas ferramentas agregadas e o software [Appium](https://appium.io/) para automatizar a consulta simulando o comportamento de um usuário comum, seja utilizando um dispositivo físico ou o emulador da plataforma.

Assim, o aplicativo funciona como uma caixa preta, não sendo necessário obter detalhes sobre sua implementação, dependendo apenas dos identificadores únicos utilizados na plataforma Android e que ficam disponíveis por questões de usabilidade da Interface de Usuário do sistema operacional.


# Pré-requisitos

## Android Studio

A primeira coisa que precisamos fazer é baixar e instalar o Android Studio, que contém o SDK de desenvolvimento do Android e algumas ferramentas agregadas que serão muito interessantes pra gente nesse caso. O download pode ser feito a partir do site oficial do Android, [neste link](https://developer.android.com/studio).


## Configurando um dispositivo

Pra gente conseguir executar o aplicativo utilizando o debugger do Android, precisamos configurar um dispositivo, seja ele físico ou virtual. Você pode utilizar um dispositivo Android conectando-o a uma porta USB do seu computador e permitindo sua utilização ativando o modo desenvolvedor. 

Outra opção é criar um dispositivo virtual que será emulado, simulando um dispositivo real. 

Não irei entrar em detalhes, pois existe amplo conteúdo cobrindo essa etapa de configuração disponível na internet. 

Recomendo que seja utilizada a versão 8.0 do sistema operacional Android, que provê a API de número 26.


## Instalando o aplicativo do SINESP

Vamos precisar do aplicativo do SINESP instalado no dispositivo, seja ele real ou virtual. Para isso você pode utilizar a própria loja de aplicativos da Google ou utilizar o comando `adb install <caminho/arquivo.apk>` para instalar um APK armazenado em seu computador. Essa etapa é importante, pois não iremos instalar o APK pelo Appium, pois não queremos modificar sua assinatura digital. O aplicativo permanecerá intacto.


## Instalando o Node

Vamos precisar do Node pra poder instalar e executar a próxima dependência do projeto. Você pode encontrar mais informações no [site oficial](https://nodejs.org/en/).


## Instalando o Appium

O Appium é o software utilizado para fazer a ponte entre o nosso script de automação (aqui o exemplo é feito em Python) e a API de debugging do Android (adb). Vamos instalar a versão 1.8.1, que foi a que eu consegui fazer funcionar com essa combinação de Android (API 26 e uiautomator2).

Podemos instalar o Appium com o comando `npm install -g appium@1.8.1` e para executar, se o Node foi instalado corretamente, basta rodar `appium` na sua linha de comando. Se você não utilizou a opção `-g` para instalar o módulo, pode ser que consiga executar com `node ./node_modules/appium/build/lib/main.js`.


## Instalando dependências do Python

Instale as dependências do Python com `pip install -r requirements.txt`.


# Executando o script

Você pode utilizar a função `search_plate` dentro do arquivo `sinesp_bot.py` ou simplesmente executar via linha de comando com `python sinesp_bot.py <placa no formato XYZ1234>`. Se você rodar a função, vai receber um dicionário com o retorno. Se rodar na linha de comando, vai receber um JSON na saída padrão. Dá pra usar essa abordagem pra integrar com outras linguagens e sistemas.


# Resolução de problemas

- O script está configurado para utilizar o emulador padrão que ganha o nome de `emulator-5554`. Você pode executar `adb devices` para obter uma lista com todos os dispoitivos. Basta trocar no dicionário `opts` no script Python.
- Verifique se o emulador está ativo e o aplicativo do SINESP está instalado.
- Se você precisar utilizar um proxy, tente configurar diretamente no emulador do Android, no seu próprio dispositivo ou no sistema operacional hospedeiro.
- Abra uma issue descrevendo seu problema caso alguma coisa tenha dado errado.


# Contribuindo

Como disse, esse repositório é uma prova de conceito e apesar se funcionar, muita coisa pode ser melhorada. Possível melhorias:

- criar um container docker com todas as dependências para execução stand-alone
- melhorar a documentação
- melhorar o código fonte
- criar e distribuir um pacote python
