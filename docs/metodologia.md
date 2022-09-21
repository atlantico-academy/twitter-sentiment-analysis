# Metodologia

O projeto tem fundamento na **metodologia CRISP-DM** para desenvolvimento das etapas de transformação de dados e produção de conhecimento de forma gerenciável.
Com esse fundamento, terá como propósito as seguintes etapas:

### 1. Proposta

Superada a fase clássica de entendimento do negócio pertinente à metologia empregada, uma vez que a base de dados foi fornecida e com tratamento de dados de sentimento dos tweets coletados de API do Twitter.

Assim, após reuniões com o squad, delimitou-se a o projeto em uma aplicação de avaliação de análise de sentimento com base no tema e palavra alvo fornecidos pelo usuário, correlacionando-os com a polaridade (positividade, neutralidade e/ou negatividade) em face do período de tempo (horário do dia e dia da semana), apresentando análises gráficas para tanto.

### 2. Entendimento

Serão consideras a proposta e a problematização do projeto para averiguação da possibilidade de adequação ao conjunto de dados e a respectiva viabilidade de execução da proposta: coleta inicial, descrição, análise exploratória e verificação de qualidade e integridade do conjunto de dados.
Em caso de necessidade, em face da contextualização e viabilidade do projeto, será submetido a reavaliação e adequação da proposta do projeto.

### 3. Preparação

Superada a etapa antecedente e produzidos os insights necessários, nessa etapa o squad distribuirá a execução das tarefas para: seleção, limpeza, construção, integração e formatação do conjunto de dados.

### 4. Modelagem

Recebido o conjunto de dados, será avaliada a necessidade de ajuste, prosseguindo ou retornando a etapa anterior, caso necessário.
Devidamente adequado, nessa etapa o squad distribuirá a execução das tarefas para: seleção da técnica, testes, construção e avaliação do modelo.

### 5. Avaliação

Aqui, superadas as etapas anteriores,  o squad distribuirá a execução das tarefas para: avaliação dos resultados, revisão do processo e definição sobre a implementação ou adequação do projeto.
Entendidas necessárias alterações ao projeto e/ou ao processo, após a revisão, proceder-se-ão às devidas adequações. 

### 6. Implantação
Por fim, na etapa final, o squad distribuirá a execução das tarefas para: planejamento da implantação, monitoração e manutenção da aplicação, relatório final e revisão do projeto.

## Fluxo de execução do projeto

``` mermaid
graph TD
    A[Análise Sentimento Twitter] -->|Obtenção base de dados| B((Proposta / Entrega 24.09))
    B -->|Contextualização e Viabilidade| C{Entendimento / Entrega 24.09 }
    C --> |Reavaliação e Adequação| B
	C -->|Insights| D((Preparação / Entrega 22.10))
    D --> E{Modelagem / Entrega 22.10}
    E -->|Ajuste| D
	E --> F{Avaliação / Entrega 19.11}
	F --> |Adaptação| B
	F --> G((Implantação / Entrega 19.11))
````

## Entregas

| Etapas | Data |
|:---:|:--:|
| 1 e 2 | 24.09.2022 |
| 3 e 4 | 22.10.2022 |
| 5 e 6 | 19.11.2022 |