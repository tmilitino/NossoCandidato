import requests

class DownloadDadosTSE:
  
  def DownloadLegenda(self,arquivoNome):
    pasta = arquivoNome.split("_")[1]
    
    resposta = requests.get(f"http://agencia.tse.jus.br/estatistica/sead/odsele/consulta_{pasta}/{arquivoNome}.zip",stream=True)

    if resposta.status_code !=200:
      raise Exception("Erro ao baixar aquivo legendas/coligacao")
    
    self._SalvarArquivo(arquivoNome,resposta)
 
  def DownloadCandidato(self,arquivoNome):
    pasta = arquivoNome.split("_")[1]
    
    resposta = requests.get(f"http://agencia.tse.jus.br/estatistica/sead/odsele/consulta_cand/{arquivoNome}.zip",stream=True)

    if resposta.status_code !=200:
      raise Exception("Erro ao baixar aquivo de candidatos")
    
    self._SalvarArquivo(arquivoNome,resposta)

  def _SalvarArquivo(self,arquivoNome, resposta):
    with open(f"pouso/{arquivoNome}.zip", 'wb') as consultaFile:
      consultaFile.write(resposta.content)