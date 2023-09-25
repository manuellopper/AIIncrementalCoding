import getpass
from github import Github, GithubException, InputGitTreeElement
import openai

# Authentication is defined via github.Auth
from github import Auth

try:
    # using an access token
    auth = Auth.Token("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")
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
    openai.api_key = "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"
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": "utiliza el código siguiente como base y genera código incremental sobre el mismo que contenga la funcionalidad indicada por el usuario"},
            {"role": "user", "content": file_content},
            {"role": "user", "content": prompt}
        ]
    )

    new_code = response['choices'][0]['message']['content'].strip()

    # Create a new branch
    source_branch = repo.get_branch("main")
    repo.create_git_ref(ref=f"refs/heads/feature-branch", sha=source_branch.commit.sha)

    # Update the file in the new branch
    if file_choice.lower() == 'n':
        repo.create_file(file_name, "Created with the help of ChatGPT", new_code, branch="feature-branch")
    else:
        repo.update_file(file.path, "Updated with the help of ChatGPT", new_code, file.sha, branch="feature-branch")

    # Create a pull request
    repo.create_pull(title="Pull Request from ChatGPT", body="Here are the changes made by ChatGPT", base="main", head="feature-branch")

except GithubException as e:
    print(f"An error occurred with GitHub: {e}")
except openai.OpenAIError as e:
    print(f"An error occurred with OpenAI: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")