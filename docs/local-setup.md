### Local setup on mac


- Install CLI packages
```shell
# Install BREW if you dont already have it. 
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required packages
brew install python3.13
brew install commitizen
brew install poetry
brew install go-task
```

- Install Docker desktop : https://www.docker.com/get-started/



### Version upgrades

```shell
cz bump --increment PATH
cz bump --increment PATH --prerelease rc
cz changelog --incremental --unreleased-version "v0.0.1"
```