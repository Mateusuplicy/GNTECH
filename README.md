
# API Clima

Esta é uma API para consulta de informações climáticas. Ela permite consultar o clima atual de diferentes cidades utilizando a OpenWeather API.

## Tecnologias

- Python
- Flask
- Docker
- Outros

## Pré-requisitos

Antes de rodar o projeto, você precisa ter as seguintes ferramentas instaladas:

- [Python](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/get-started)
- [Git](https://git-scm.com/)

## Como rodar o projeto

### Passo 1: Clone o repositório

Se você ainda não tem o repositório clonado, pode fazer isso com o comando:

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
```
### Passo 2: Instale as dependências
Entre no diretório do seu projeto e instale as dependências com:

```bash
cd nome-do-projeto
pip install -r requirements.txt
```
### Passo 3: Rodando o Docker
Para rodar o projeto dentro de um container Docker, use os seguintes comandos:

```bash
docker build -t minha-api-clima .
docker run -d -p 5000:5000 minha-api-clima
```
### Passo 4: Acessando a aplicação
Abra o navegador e acesse a aplicação em:
```bash
http://127.0.0.1:5000/clima
```
