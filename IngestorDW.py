import postgresql
import configparser
import pandas as pd
import os

class Ingestor():
  
  
  def _AbrirConfig(self):

    config = configparser.ConfigParser()
    config.read("CONFIG/GERAL.CFG")

    self.user = config["DEFAULT"]["user"]
    self.senha = config["DEFAULT"]["pass"]
    self.host = config["DEFAULT"]["host"]
    self.port = config["DEFAULT"]["port"]
    self.database = config["DEFAULT"]["database"]
    self.dirBase = config["DEFAULT"]["dirBase"]

  def _ConectaDW(self):

    return postgresql.open(f'pq://{self.user}:{self.senha}@{self.host}:{self.port}/{self.database}')  

  def _ListarArquivos(self,caminho)->list:

    return [f for f in os.listdir(caminho) if os.path.isfile(f"{caminho}/{f}")]

  def _Preparacao(self, ConexaoDW, tabela:str, colunas:list):

    listaIndex = [f"${colunas.index(valor)+1}" for valor in colunas]

    colunasOrdem = ", ".join(listaIndex)

    queryInsert = f'INSERT INTO {tabela} ({", ".join(colunas)}) VALUES ({colunasOrdem})'

    return ConexaoDW.prepare(queryInsert)

  def _ListarDado(self, Caminho, ListaArquivos):
    data = list()
    for arquivo in ListaArquivos:
        with open(f"{Caminho}/{arquivo}",'r') as myfile:
            arq = myfile.readlines()
            head = arq[0].replace("\n","").replace('"',"").split(";")
            for linha in arq[1:]:
              data.append(linha.replace("\n","").replace('"',"").split(";"))


    return pd.DataFrame(data, columns=head)

  def _DadosCaptura(self)->dict:
    pass

  def StartIngestor(self, NomePasta:str, Ano:str):
    
    self._AbrirConfig()
    conexo = self._ConectaDW()
    lArquivo = self._ListarArquivos(self.dirBase.format(NomePasta, Ano))
    df = self._ListarDado(self.dirBase.format(NomePasta, Ano),lArquivo)

    insertFunc = self._Preparacao(conexo,"partidos", ['legenda', "nome_partido", "sigla"])
    
    te = ["NR_PARTIDO","SG_PARTIDO","NM_PARTIDO"]

    dfLegenda = df[te].drop_duplicates().reset_index()
    
    print(dfLegenda.shape)

    dfLegenda["NR_PARTIDO"] = dfLegenda["NR_PARTIDO"].astype(int)

    dfLegenda.apply( lambda x: insertFunc.load_rows([tuple(x[te])]),axis=1)
    insertFunc.close()




