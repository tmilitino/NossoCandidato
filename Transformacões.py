

tabela ="teste"
colunas = ["test1", "teste2","teste3"]

listaIndex = [f"${colunas.index(valor)+1}" for valor in colunas]
print(listaIndex)


colunasOrdem = ", ".join(listaIndex)


queryInsert = f'INSERT INTO {tabela} ({", ".join(colunas)}) VALUES ({colunasOrdem})'
print(queryInsert)