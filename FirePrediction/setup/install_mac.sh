
# make sure homebrew is up-to-date and install some stuff
brew update
brew install postgres || brew upgrade postgres
brew install postgis || brew upgrade postgis
brew install jq
