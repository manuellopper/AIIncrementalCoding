import getpass
from github import Github, GithubException, InputGitTreeElement
import openai
from config import api_key_openai, api_key_github
import random
import string

# Authentication is defined via github.Auth
from github import Auth

try:
    # using an access token
    auth = Auth.Token(api_key_github)
    # Connect to the repository
    g = Github(auth=auth)
    user = g.get_user()

    # List all repositories and allow the user to choose one
    print("Your repositories:")
    repos = list(user.get_repos())
    for i, repo in enumerate(repos):
        print(f"{i+1}. {repo.name}")
    repo_choice = int(input("Choose the number of the repository you want to work on: ")) - 1
    repo = repos[repo_choice]

    # Ask the user if they want to work on an existing file or create a new one
    file_choice = input("Do you want to work on an existing file (E) or create a new one (N)? ")

    if file_choice.lower() == 'n':
        # Ask the user to enter the name of the file
        file_name = input("Enter the name of the new file: ")
        file_content = ""
    else:
        # Show all project files and allow the user to choose one
        print("Files in this repository:")
        files = repo.get_contents("")
        for i, file in enumerate(files):
            print(f"{i+1}. {file.path}")
        num_file_choice = int(input("Choose the number of the file you want to work on: ")) - 1
        file = files[num_file_choice]
        file_content = file.decoded_content.decode()

    # Ask the user how the AI can help
    prompt = input("How can the AI help you write code? ")

    # Invoke the ChatGPT API
    openai.api_key = api_key_openai
    response = openai.ChatCompletion.create(
      model="gpt-4",
      messages=[
            {"role": "system", "content": "utiliza el código siguiente como base y genera código incremental sobre el mismo que contenga la funcionalidad indicada por el usuario. En la respuesta escribe solo codigo, no realices ninguna aclaracion ni antes ni despues de este"},
            {"role": "user", "content": file_content},
            {"role": "user", "content": prompt}
        ],
      temperature=0
    )

    new_code = response['choices'][0]['message']['content'].strip()

    # Create a new branch
    source_branch = repo.get_branch("main")
    branch_name = "new_branch"
    while True:
        try:
            repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=source_branch.commit.sha)
            break
        except GithubException:
            branch_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

    print(f"New branch created: {branch_name}")

    # Update the file in the new branch
    if file_choice.lower() == 'n':
        repo.create_file(file_name, "Created with the help of ChatGPT", new_code, branch=branch_name)
    else:
        repo.update_file(file.path, "Updated with the help of ChatGPT", new_code, file.sha, branch=branch_name)

    # Create a pull request
    repo.create_pull(title="Pull Request from ChatGPT", body="Here are the changes made by ChatGPT", base="main", head=branch_name)

    print("Success! The operations were completed successfully.")

    # Provide a summary of the tasks performed
    print("\nSummary of tasks performed:")
    print(f"1. Connected to the repository: {repo.name}")
    print(f"2. Created a new branch: {branch_name}")
    if file_choice.lower() == 'n':
        print(f"3. Created a new file: {file_name}")
    else:
        print(f"3. Updated the existing file: {file.path}")
    print("4. Created a pull request")

except GithubException as e:
    print(f"An error occurred with GitHub: {e}")
except openai.OpenAIError as e:
    print(f"An error occurred with OpenAI: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")