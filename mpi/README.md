# Brief MPI - Ajustado

Este pacote implementa o cálculo do Prognóstico Multidimensional Índice Ajustado  (Brief MPI - Ajustado) para avaliação de fragilidade em idosos, com base nos dados coletados no REDCap nas ILPI's.

## Instalação

Clone o repositório e importe como módulo local, ou integre ao seu projeto Python.

## Uso

```python
from mpi import aplicar_brief_mpi

def main():
    df = pd.read_csv("data/SMSAp/lake/mpiFinal.csv")
    df_resultado = aplicar_brief_mpi(df)
    #print(df_resultado[["uuidv5", "MPI", "risk"]])
    df_resultado.head()
    df_resultado.to_csv("data/SMSAp/lake/mpiScore.csv")
    print("✅Tabela MPI Score foi salva no lake!")
    print(df_resultado.head())

if __name__ == "__main__":
    main()

