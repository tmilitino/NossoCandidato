import configparser
import zipfile
import os

class Ingestor(object):

  def _AbrirConfig(self):
    
    config = configparser.ConfigParser()
    config.read("CONFIG/GERAL_Captura.CFG")

    self.dirPouso = config["DEFAULT"]["dirPouso"]
    self.dirBase = config["DEFAULT"]["dirBase"]
    self.mDirBase = config["DEFAULT"]["mDirBase"]
  
  def _criarParticao(self, Pasta, Particao:str)->bool:
   
    if not os.path.isdir("/".join([Pasta, Particao])):
      os.mkdir("/".join([Pasta, Particao]))
      return True
    
    return False

  def _criarPasta(self, Tabela:str)->str:
    
    pathTabela = self.mDirBase.format(Tabela)
    if not os.path.isdir(pathTabela):
      os.mkdir(pathTabela)
    
    return pathTabela

  def _unzip(self,NomeArquivo, PathFinal):
    with zipfile.ZipFile(self.dirPouso.format(NomeArquivo), 'r') as zip_ref:
      zip_ref.extractall(PathFinal)
    
  
  def _deletarPouso(self,NomeArquivo):
    os.remove(self.dirPouso.format(NomeArquivo))
    
  def DescompactadorArquivo(self, NomeArquivo:str):
    
    tabela = "_".join(NomeArquivo.split("_")[0:2])

    particao = NomeArquivo.split("_")[-1]

    tabelaFinal = self._criarPasta(tabela)

    self._criarParticao(tabelaFinal, particao)
    
    self._unzip(NomeArquivo, self.dirBase.format(tabela,particao))

    self._deletarPouso(NomeArquivo)