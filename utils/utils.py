# ------------------------------
# Funções utilitárias
# ------------------------------

def criar_diretorios():
    import os
    os.makedirs('../tables', exist_ok=True)
    os.makedirs('../plots', exist_ok=True)
    os.makedirs('../../../../data/SMSAp/Lake', exist_ok=True)
