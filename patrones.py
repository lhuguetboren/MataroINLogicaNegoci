import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.preprocessing import TransactionEncoder

#transformar la tabla cookies en un array de la siguiente fomra

arra=[['']]

# Definir el array de transacciones
array = [['x','a', 'b', 'c'], ['y','a', 'b', 'c'], ['a', 'd', 'a','b','c']]

# Codificar las transacciones
te = TransactionEncoder()
te_array = te.fit(array).transform(array)
df = pd.DataFrame(te_array, columns=te.columns_)

# Aplicar Apriori para encontrar patrones frecuentes
patrones = apriori(df, min_support=0.5, use_colnames=True)

# Filtrar patrones que tienen 3 o más elementos
patrones_3_o_mas = patrones[patrones['itemsets'].apply(lambda x: len(x) >= 3)]

# Encontrar el patrón más frecuente (con el soporte más alto)
patron_mas_comun = patrones_3_o_mas.sort_values(by='support', ascending=False).head(1)

# Mostrar el patrón más frecuente con 3 o más elementos
print(patron_mas_comun)
