# import Descompactador
import IngestorDW
import Transformacoes


ListaAno = [2018]

for ano in ListaAno:
  nomeArquivo = f"consulta_coligacao_{ano}"
  # DownloadDados.DownloadDadosTSE().DownloadLegenda(nomeArquivo)
  
  IngestorDW.Ingestor().StartIngestor(nomeArquivo)