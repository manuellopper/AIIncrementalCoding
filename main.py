try:
    # Resto del código

    # Create a pull request
    pull_request = repo.create_pull(title="Pull Request from ChatGPT", body="Here are the changes made by ChatGPT", base="main", head="feature-branch")
    
    # Print success message
    print("\nCode generated successfully!")
    print(f"\nSummary of changes:")
    if file_choice.lower() == 'n':
        print(f"New file created: {file_name}")
        print(f"New code added to {file_name}:\n{new_code}")
    else:
        print(f"File updated: {file.path}")
        print(f"Modified code in {file.path}:\n{new_code}")
    print(f"\nPull Request created: {pull_request.html_url}")

except GithubException as e:
    # Resto del código

# Resto del código