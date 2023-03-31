import os
import re
import csv

# Define as extensões dos arquivos que serão analisados
extensions = ['.js', '.php', '.feature', '.vue', '.py', '.sh']

# Define o padrão para identificar os comentários em cada linguagem
patterns = {
    '.js': r'(\/\/.*)|(\/\*[\s\S]*?\*\/)',
    '.php': r'(\/\/.*)|(\/\*[\s\S]*?\*\/)',
    '.feature': r'(^|\s)#.*$',
    '.vue': r'(\/\/.*)|(\/\*[\s\S]*?\*\/)',
    '.py': r'(^\s*#.*$)|(^[\t ]*""".*"""[\t ]*$)',
    '.sh': r'(^\s*#.*$)'
}

# Define o caminho do diretório do repositório
repo_path = 'nextcloud/spreed'

# Define o caminho do diretório local onde os arquivos serão baixados
local_path = 'spreed_repo'

# Faz o clone do repositório para o diretório local
os.system(f'git clone https://github.com/{repo_path}.git {local_path}')

# Lista os arquivos do diretório local com as extensões definidas
files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(local_path) for f in filenames if os.path.splitext(f)[1] in extensions]

# Cria um arquivo CSV para armazenar os resultados
with open('comments.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['filename', 'line_number', 'comment']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    # Percorre cada arquivo e busca pelos comentários
    for file in files:
        with open(file, mode='r', encoding='utf-8') as f:
            lines = f.readlines()

        # Para cada linha, verifica se contém um comentário
        for i, line in enumerate(lines, 1):
            for ext, pattern in patterns.items():
                if file.endswith(ext):
                    comments = re.findall(pattern, line)
                    for comment in comments:
                        if comment != '':
                            writer.writerow({'filename': file, 'line_number': i, 'comment': comment[0]})
                            break
