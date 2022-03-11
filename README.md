Minha Primeira Simulação em Python Mesa
=========================================
Resumo
------------

Este projeto usa [Mesa](https://github.com/projectmesa/mesa) para rodar o modelo de simulação, no qual um fogo se inicializa em uma floresta, a qual é uma grade de células as quais podem ser vazias ou conter uma árvore, e acaba se alastrando por ela. O fogo se espalha de cada árvore que estea pegando fogo para as árvores vizinhas que não estejam queimadas, cada árvore tem o status de: em chamas, queimada ou não queimada. Este repositorio realiza uma modificação no modelo original ([Forest Fire](https://github.com/projectmesa/mesa/tree/main/examples/forest_fire)), onde é inserido um novo agente de vento e barreiras de incêndio que controlam o direcional e impedem o fogo.  

Como inicializar o servidor
------------

Para rodar o modelo, execute o comando no diretório do projeto:
```bash
$ mesa runserver
```
