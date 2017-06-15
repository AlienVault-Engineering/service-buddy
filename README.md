# service-manager
## Installation

 virtualenv ./venv
./venv/bin/pip install --upgrade pybuilder==0.11.9
pyb install

## Usage

usage: service-manager [-h] [--verbose]
                       [--application-filter APPLICATION_FILTER] --vcs-user
                       VCS_USER --vcs-password VCS_PASSWORD
                       [--repo-root REPO_ROOT]
                       [--service-directory SERVICE_DIRECTORY] [--dry-run]
                       {list,sync,pull} ...

Utility to help deploy and manage microservices.

positional arguments:
  {list,sync,pull}      commands
    list                List known services
    sync                Sync service definitions and initialize new entries.
    pull                Pull git repos into local filesystem.

optional arguments:
  -h, --help            show this help message and exit
  --verbose             Level of logging to output
  --application-filter APPLICATION_FILTER
                        Constrain to passed application
  --vcs-user VCS_USER   Username for VCS
  --vcs-password VCS_PASSWORD
                        Password for VCS
  --repo-root REPO_ROOT
                        Root user for BitBucket
  --service-directory SERVICE_DIRECTORY
                        Directory containing service definitions in
                        <app>/service.json format
  --dry-run             Preview effect of action
  
  
  
