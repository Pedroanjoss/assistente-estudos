
1. Descrição do Projeto
Este trabalho é um Agente Inteligente (Assistente Virtual) conforme solicitado nas especificações da disciplina. O "mini-mundo" (escopo) escolhido é um Tutor de Estudos Pessoal, focado na automação de tarefas acadêmicas, como organização de rotinas e gerenciamento de tarefas.

O projeto utiliza Python, a biblioteca transformers (para o modelo Wav2Vec2 do Hugging Face) e NLTK para o processamento de áudio e linguagem.

2. Instruções de Instalação e Execução
Para executar este projeto, siga os passos abaixo na ordem correta.

Passo 1: Pré-requisitos
Python 3.+ instalado no sistema.

Um microfone funcional (para o modo de demonstração ao vivo).

Passo 2: Configuração do Ambiente
Estes comandos devem ser executados no seu terminal (CMD ou PowerShell) dentro da pasta do projeto.

1. Crie o Ambiente Virtual (venv)

python -m venv .venv

2. Ative o Ambiente Virtual

.\.venv\Scripts\activate

(O prompt do seu terminal deve agora mostrar (.venv) no início)

3. Instale as Dependências Python

Este comando irá instalar todas as bibliotecas do requirements.txt.

Bash

pip install  -r requirements.txt


4. Baixe os Pacotes de Dados NLTK

O NLTK (usado para word_tokenize e stopwords) precisa de pacotes de dados que não são instalados pelo pip. O script inicializar_nltk.py foi criado para baixar todos os pacotes necessários (como punkt, punkt_tab e stopwords).

python inicializar_nltk.py


3. Como Executar o Projeto
Existem duas formas de rodar o assistente, ambas necessárias para a avaliação.

Execução 1: Testes Automatizados (Requisito 9)
Este modo executa os testes unitários (testes.py) usando os arquivos de áudio pré-gravados na pasta /audios. Este teste valida toda a cadeia: Áudio -> Transcrição -> Tokenização -> Validação (config.json) -> Atuação.

Bash

python testes.py
Saída Esperada: O terminal mostrará o resultado de cada teste (com as transcrições) e terminará com Ran 5 tests in ...s e OK.

Execução 2: Assistente Ao Vivo (Modo Demonstração)
Este modo ativa o MODO_LINHA_DE_COMANDO e escuta o microfone do seu computador.

Bash

python assistente-estudos.py
Saída Esperada:

O sistema mostrará "Atuador 'Plano' iniciado.", "Atuador 'Revisão' iniciado.", etc.

Aguardará com a mensagem "fale alguma coisa..."

Após 5 segundos, mostrará "fala capturada".

Em seguida, exibirá o comando tokenizado (ex: ['adicionar', 'revisão', '...']) e o resultado da ação do atuador (ex: [ATUADOR REVISÃO]: ...).

4. Estrutura dos Arquivos
assistente-estudos.py: O "cérebro" principal que gerencia o fluxo.

/audios/: Contém os 4 áudios .wav usados pelo testes.py.

config.json: Arquivo de configuração externo (Requisito 'a') que mapeia os comandos de voz, incluindo variações de fala (ex: "planos", "marca", "gerá rezão").

plano.py, revisao.py, tarefa.py, resumo.py: Os 4 atuadores (Requisito 'c').

transcritor.py: Módulo que carrega o modelo de IA e converte áudio em texto. (Modificado para usar backend="soundfile" e evitar o erro do torchcodec).

testes.py: Script de unittest (Requisito 9).

inicializar_nltk.py: Script de setup para baixar dados do NLTK.

requirements.txt: Lista de dependências Python.

README.md: Este arquivo.