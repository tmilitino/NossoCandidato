import postgresql
import configparser
import pandas as pd
import os

class Ingestor():
  
  
  def _abrirConfig(self):

    config = configparser.ConfigParser()
    config.read("CONFIG/GERAL.CFG")

    self.user = config["DEFAULT"]["user"]
    self.senha = config["DEFAULT"]["pass"]
    self.host = config["DEFAULT"]["host"]
    self.port = config["DEFAULT"]["port"]
    self.database = config["DEFAULT"]["database"]

  def _conectaDW(self):

    return postgresql.open(f'pq://{self.user}:{self.senha}@{self.host}:{self.port}/{self.database}')  

  def _listarArquivos(self,caminho)->list:

    return [f for f in os.listdir(caminho) if os.path.isfile(f"{caminho}/{f}")]

  def _Preparacao(self, ConexaoDW, tabela:str, colunas:list):

    listaIndex = [f"${colunas.index(valor)+1}" for valor in colunas]

    colunasOrdem = ", ".join(listaIndex)

    queryInsert = f'INSERT INTO {tabela} ({", ".join(colunas)}) VALUES ({colunasOrdem})'

    return ConexaoDW.prepare(queryInsert)

  def _listarDado(self, Caminho, ListaArquivos):
    data = list()
    for arquivo in ListaArquivos:
        with open(f"{Caminho}/{arquivo}",'r') as myfile:
            arq = myfile.readlines()
            head = arq[0].replace("\n","").replace('"',"").split(";")
            for linha in arq[1:]:
              data.append(linha.replace("\n","").replace('"',"").split(";"))


    return pd.DataFrame(data, columns=head)

  def StartIngestor(self, NomeArquivo):
    
    self._abrirConfig()
    conexo = self._conectaDW()
    larqi = self._listarArquivos("base/consulta_coligacao/2018")
    df = self._listarDado("base/consulta_coligacao/2018",larqi)

    insertLegenda = self._Preparacao(conexo,"partidos", ['legenda', "nome_partido", "sigla"])

    dfLegenda = df[["NR_PARTIDO","SG_PARTIDO","NM_PARTIDO"]].drop_duplicates().reset_index()
    
    dfLegenda["NR_PARTIDO"] = dfLegenda["NR_PARTIDO"].astype(int)

    dfLegenda.apply( lambda x: insertLegenda.load_rows([tuple(x[["NR_PARTIDO","NM_PARTIDO","SG_PARTIDO"]])]),axis=1)
    insertLegenda.close()




