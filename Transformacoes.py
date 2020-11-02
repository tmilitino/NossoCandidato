import postgresql
import configparser


class Transformacao():

  def _abrirConfig(self):

    config = configparser.ConfigParser()
    config.read("CONFIG/GERAL_Captura.CFG")

    self.user = config["DEFAULT"]["user"]
    self.senha = config["DEFAULT"]["pass"]
    self.host = config["DEFAULT"]["host"]
    self.port = config["DEFAULT"]["port"]
    self.database = config["DEFAULT"]["database"]

  def _conectaCaptura(self):
    
    return postgresql.open(f'pq://{self.user}:{self.senha}@{self.host}:{self.port}/{self.database}')


  def _selectColunas(self, Tabela):
    db = self._conectaCaptura()
    sql = f"select nome_coluna from colunas where tabela = {Tabela}"
    rs=db.prepare(sql)
    db.close()
    return [linha for linha in rs]

  def ListaColunas(self, df, insertLegenda):
    ListaColunas = self._selectColunas("teste")
    
    dfLegenda = df[ListaColunas].drop_duplicates().reset_index()


    dfLegenda.apply( lambda x: insertLegenda(int(x["NR_PARTIDO"]),x["NM_PARTIDO"],x["SG_PARTIDO"]),axis=1)
