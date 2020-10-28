import Descompactador
import DownloadDados


ListaAno = [2018,2020]

for ano in ListaAno:
  nomeArquivo = f"consulta_coligacao_{ano}"
  DownloadDados.DownloadDadosTSE().DownloadLegenda(nomeArquivo)
  
  Descompactador.Descompactador().DescompactadorArquivo(nomeArquivo)