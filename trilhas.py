import os
from datetime import datetime
import pandas as pd
import traceback
from traceback import format_exc as trace

def processar_telefones_por_arquivo(arquivo_entrada, arquivo_saida_base): 
    try: 
        df = pd.read_csv(arquivo_entrada, sep=';', dtype=str) 
        total_linhas = len(df) 
        linhas_por_arquivo = total_linhas // 3 
        arquivos_saida = [ f"{arquivo_saida_base}_parte1.csv", f"{arquivo_saida_base}_parte2.csv", f"{arquivo_saida_base}_parte3.csv" ] 
        for i, arquivo_saida in enumerate(arquivos_saida): 
            with open(arquivo_saida, 'w', encoding='utf-8') as f: 
                f.write('cpf_cnpj;ddd;telefone;obs_telefone\n') 
                inicio = i * linhas_por_arquivo 
                fim = (i + 1) * linhas_por_arquivo if i < 2 else total_linhas 
                for index, row in df.iloc[inicio:fim].iterrows(): 
                    cpf = str(row['cpfcnpj']).zfill(14) 
                    for j in range(1, 5): 
                        telefone = row.get(f'telefone{j}', None) 
                        if pd.notna(telefone): 
                            telefone = str(telefone).replace('.0', '') 
                            ddd = telefone[:2] 
                            numero_sem_ddd = telefone[2:]
                            if len(numero_sem_ddd) >= 8:
                                f.write(f'{cpf};{ddd};{numero_sem_ddd};Telefone Projeto Trilha ASCOB\n') 
    except: 
        print(f'Ocorreu um erro ao processar o arquivo de entrada.\n{trace()}')

def pegar_base_automatica():
    try:
        data_atual = datetime.now().strftime('%Y%m%d')
        pasta_base = r'C:\OER_MIS\py_library\060_cargas_poc\Bases_originais_Ascob'
        nome_base = f"ramos_trilha_tel_var_{data_atual}_unificado"
        
        caminho_com_txt = os.path.join(pasta_base, f"{nome_base}.txt")
        
        if os.path.exists(caminho_com_txt):
            print(f"Arquivo encontrado: {caminho_com_txt}")
            return caminho_com_txt
        else:
            print(f"Procurando por: {caminho_com_txt}")
            print("Arquivos disponíveis na pasta:")
            if os.path.exists(pasta_base):
                for f in os.listdir(pasta_base):
                    print(f" - {f}")
            raise FileNotFoundError(f"Nenhum arquivo correspondente a '{nome_base}" foi encontrado.")
            
    except Exception as e:
        print(f"Ocorreu um erro ao localizar o arquivo de entrada.\n{traceback.format_exc()}")
        return None

print('Iniciando robô...')
arquivo_entrada = pegar_base_automatica()

if arquivo_entrada:
    data_atual = datetime.now().strftime('%Y%m%d')
    pasta_destino = r'Z:\10-MIS\- MIS_NEW\CLIENTES\ASCOB\TRILHA ASCOB(1)\Arquivos_gerados'
    
    os.makedirs(pasta_destino, exist_ok=True)
    
    arquivo_saida_base = os.path.join(pasta_destino, f"Trilha_{data_atual}")
    
    print(f"Gerando arquivos de saída em: {pasta_destino}")
    processar_telefones_por_arquivo(arquivo_entrada, arquivo_saida_base)
    print('Processamento concluído com sucesso!')

try:
    input('Pressione qualquer tecla para sair...')
except:
    pass