# API de Sorteio de Amigo Oculto 🎉

Este projeto foi desenvolvido para a API|G-F de Natal, onde deveríamos criar a própria API para realizar sorteios de amigo oculto. Desenvolvido por João Carlos e Mariana Andrade, utilizamos FASTAPI para criar as rotas, estas que estão funcionando perfeitamente.

## Organização do Projeto

Durante o horário destinado à atividade, organizamos os arquivos do projeto aplicando o conceito de **Responsabilidade Única (SRP)**, o que melhorou a estrutura e manutenção do código. 
Além disso, iniciamos a implementação de autenticação para as rotas, mas não conseguimos finalizar essa funcionalidade a tempo.

## Banco de dados

Foi utilizado o banco de dados SQLite para armazenamento dos dados.

## Rotas da API

A API possui as seguintes rotas principais:

### **Usuários**
- `POST /usuarios/cadastrar_amigo`: Cadastra novos amigos para participar dos sorteios.
- `GET /usuarios/perfis`: Retorna os perfis dos usuários cadastrados.

### **Grupos**
- `POST /grupos/criar_grupo`: Cria um novo grupo para o sorteio.
- `GET /grupos/grupos`: Lista todos os grupos criados.

### **Participações**
- `POST /participacoes/add_amigo`: Adiciona um amigo a um grupo específico.

### **Sorteios**
- `POST /sorteios/gerar_match`: Realiza o sorteio e gera atribui o amigo sorteado para cada participante.
- `GET /sorteios/resultados/{grupoId}`: Consulta os resultados do sorteio de um grupo, utilizando o ID do grupo.

## Pendências

- **Autenticação**: A funcionalidade de autenticação foi iniciada, mas ainda não foi finalizada. 

## Conclusão

Apesar de algumas funcionalidades ainda não estarem completas, avançamos significativamente na organização do projeto e na implementação das rotas principais. Esta API está pronta para realizar sorteios de amigo oculto de forma prática e funcional. 


