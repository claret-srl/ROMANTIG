find $(pwd) -type f -not -path "*.git*" -not -path "*.dev*" -not -path "*.vscode*" -print0 | xargs -0 dos2unix --