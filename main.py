Para implementar la funcionalidad solicitada, necesitamos extraer el contenido del código entre los marcadores <python> y </python> de la respuesta de la API de OpenAI. Podemos hacer esto utilizando expresiones regulares (regex) para buscar y extraer el contenido entre estos marcadores. Aquí está el código modificado:

<python>
# Importando las bibliotecas necesarias
import getpass
from github import Github, GithubException, InputGitTreeElement
import openai
from config import api_key_openai, api_key_github
import random
import string
import re
from github import Auth

try:
    # Autenticación en GitHub
    auth = Auth.Token(api_key_github)
    g = Github(auth=auth)
    user = g.get_user()

    # Mostrando los repositorios del usuario
    print("Your repositories:")
    repos = list(user.get_repos())
    for i, repo in enumerate(repos):
        print(f"{i+1}. {repo.name}")

    # Permitiendo al usuario seleccionar un repositorio
    repo_choice = int(input("Choose the number of the repository you want to work on: ")) - 1
    repo = repos[repo_choice]

    # Permitiendo al usuario seleccionar un archivo existente o crear uno nuevo
    file_choice = input("Do you want to work on an existing file (E) or create a new one (N)? ")
    if file_choice.lower() == 'n':
        file_name = input("Enter the name of the new file: ")
        file_content = ""
    else:
        # Mostrando los archivos en el repositorio seleccionado
        print("Files in this repository:")
        files = repo.get_contents("")
        for i, file in enumerate(files):
            print(f"{i+1}. {file.path}")

        # Permitiendo al usuario seleccionar un archivo
        num_file_choice = int(input("Choose the number of the file you want to work on: ")) - 1
        file = files[num_file_choice]
        file_content = file.decoded_content.decode()

    # Solicitando al usuario que indique cómo puede ayudarle la IA
    prompt = input("How can the AI help you write code? ")

    # Autenticación en OpenAI
    openai.api_key = api_key_openai

    # Generando código con la ayuda de la IA
    response = openai.ChatCompletion.create(
      model="gpt-4",
      messages=[
            {"role": "system", "content": "utiliza el código siguiente como base y genera código incremental sobre el mismo que contenga la funcionalidad indicada por el usuario. En la respuesta, cuando vayas a escribir el código en python precede éste con <python>  y utiliza </python> para terminar el bloque de código. "},
            {"role": "user", "content": file_content},
            {"role": "user", "content": prompt}
        ],
      temperature=0
    )
    full_response = response['choices'][0]['message']['content'].strip()

    # Extracting the code between the <python> and </python> markers
    new_code = re.search('<python>(.*?)</python>', full_response, re.DOTALL).group(1).strip()

    # Creando una nueva rama en el repositorio
    source_branch = repo.get_branch("main")
    branch_name = "new_branch"
    while True:
        try:
            repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=source_branch.commit.sha)
            break
        except GithubException:
            branch_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

    # Creando o actualizando el archivo con el nuevo código
    if file_choice.lower() == 'n':
        repo.create_file(file_name, "Created with the help of ChatGPT", new_code, branch=branch_name)
    else:
        repo.update_file(file.path, "Updated with the help of ChatGPT", new_code, file.sha, branch=branch_name)

    # Creando una solicitud de extracción
    repo.create_pull(title="Pull Request from ChatGPT", body="Here are the changes made by ChatGPT", base="main", head=branch_name)

    # Resumen de las tareas realizadas
    print("Success! The operations were completed successfully.")
    print("\nSummary of tasks performed:")
    print(f"1. Connected to the repository: {repo.name}")
    print(f"2. Created a new branch: {branch_name}")
    if file_choice.lower() == 'n':
        print(f"3. Created a new file: {file_name}")
    else:
        print(f"3. Updated the existing file: {file.path}")
    print("4. Created a pull request")

# Manejo de excepciones
except GithubException as e:
    print(f"An error occurred with GitHub: {e}")
except openai.OpenAIError as e:
    print(f"An error occurred with OpenAI: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
</python>