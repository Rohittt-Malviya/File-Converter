# Security

Files are processed locally. The applications do not execute input files, call conversion APIs, or send file contents to remote services. Inputs are checked for existence, non-empty content, and selected format signatures where practical. Outputs are created without overwriting existing files.
