from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torchaudio
import torch

MODELO = "lgris/wav2vec2-large-xlsr-open-brazilian-portuguese-v2"

AUDIOS = [
    {
        "comando": "Mostrar plano de estudos",
        "wav": "C:\\Users\\Pedro\\Documents\\atividade\\assistente-estudos\\audios\\plano-estudo.wav"
    },
    {
        "comando": "Adicionar revisão",
        "wav": "C:\\Users\\Pedro\\Documents\\atividade\\assistente-estudos\\audios\\adicionar-revisao.wav"
    },
    {
        "comando": "Marcar tarefa",
        "wav": "C:\\Users\\Pedro\\Documents\\atividade\\assistente-estudos\\audios\\marcar-tarefa.wav"
    },
    {
        "comando": "Gerar resumo",
        "wav": "C:\\Users\\Pedro\\Documents\\atividade\\assistente-estudos\\audios\\gerar-resumo.wav"
    }
]

def iniciar_modelo(nome_modelo, dispositivo="cpu"):
    iniciado, processador, modelo = False, None, None

    try:
        processador = Wav2Vec2Processor.from_pretrained(nome_modelo)
        modelo = Wav2Vec2ForCTC.from_pretrained(nome_modelo).to(dispositivo)

        iniciado = True
    except Exception as e:
        print(f"erro iniciando o modelo: {str(e)}")

    return iniciado, processador, modelo

TAXA_AMOSTRAGEM = 16_000

def carregar_fala(caminho_audio):
    audio, amostragem = torchaudio.load(caminho_audio)
    if audio.shape[0] > 1:
        audio = torch.mean(audio, dim=0, keepdim=True)

    if amostragem != TAXA_AMOSTRAGEM:
        adaptador_amostragem = torchaudio.transforms.Resample(amostragem, TAXA_AMOSTRAGEM)
        audio = adaptador_amostragem(audio)

    return audio.squeeze()

def transcrever_fala(dispositivo, fala, modelo, processador):
    entrada = processador(fala, return_tensors="pt", sampling_rate=TAXA_AMOSTRAGEM).input_values.to(dispositivo)
    saida = modelo(entrada).logits

    predicao = torch.argmax(saida, dim=-1)
    transcricao = processador.batch_decode(predicao)[0]

    return transcricao.lower()

if __name__ == "__main__":
    dispositivo = "cuda:0" if torch.cuda.is_available() else "cpu"

    iniciado, processador, modelo = iniciar_modelo(MODELO, dispositivo)
    if iniciado:
        for audio in AUDIOS:
            print(f"testando transcrição do comando: {audio['comando']}")

            fala = carregar_fala(audio["wav"])
            transcricao = transcrever_fala(dispositivo, fala, modelo, processador)

            print(f"transcrição: {transcricao}")