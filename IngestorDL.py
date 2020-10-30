import zipfile
import os

class Ingestor(object):
  
  def _criarParticao(self, Pasta, Particao:str)->bool:
   
    if not os.path.isdir("/".join([Pasta, Particao])):
      os.mkdir("/".join([Pasta, Particao]))
      return True
    
    return False


  def _criarPasta(self, Tabela:str)->str:
    """ Cria Pasta da tabela"""

    pathTabela = f"base/{Tabela}"
    if not os.path.isdir(pathTabela):
      os.mkdir(pathTabela)
    
    return pathTabela

  def _unzip(self,NomeArquivo, PathFinal):
    with zipfile.ZipFile(f"pouso/{NomeArquivo}.zip", 'r') as zip_ref:
      zip_ref.extractall(PathFinal)
    
  
  def _deletarPouso(self,NomeArquivo):
    os.remove(f"pouso/{NomeArquivo}.zip")
    

  def DescompactadorArquivo(self, NomeArquivo:str):
    
    tabela = "_".join(NomeArquivo.split("_")[0:2])

    particao = NomeArquivo.split("_")[-1]

    tabelaFinal = self._criarPasta(tabela)

    self._criarParticao(tabelaFinal, particao)
    
    self._unzip(NomeArquivo, f"base/{tabela}/{particao}")

    self._deletarPouso(NomeArquivo)