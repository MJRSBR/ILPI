# %%
import pandas as pd
from mpi import aplicar_brief_mpi  

# %%
def main():
    df = pd.read_csv("data/SMSAp/lake/mpiFinal.csv")
    df_resultado = aplicar_brief_mpi(df)
    df_resultado.head()
    df_resultado.to_csv("data/SMSAp/lake/mpiScore.csv")
    print("✅Tabela MPI Score foi salva no lake!")
    print(df_resultado.head())

if __name__ == "__main__":
    main()

# %%
