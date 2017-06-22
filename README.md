# service-manager

[Build Status](https://api.travis-ci.org/AlienVault-Engineering/service-manager.png) 
## Installation

```bash
virtualenv ./venv
./venv/bin/pip install --upgrade pybuilder==0.11.9
pyb install
```

## Usage

```bash
Utility to help deploy and manage microservices.

positional arguments:
  {list,sync,pull}      commands
    list                List known services
    sync                Sync service definitions and initialize new entries.
    pull                Pull git repos into local filesystem.

optional arguments:
  -h, --help            show this help message and exit
  
  --verbose             Level of logging to output
  
  --application-filter  Constrain processing to passed application root
    APPLICATION_FILTER 
    
  --vcs-user            Username for VCS
    VCS_USER   
    
  --vcs-password        Password for VCS
    VCS_PASSWORD 
    
  --vcs-root-url        Root url for git repos
    VCS_ROOT_URL 
    
  --service-directory   Directory containing service definitions in
    SERVICE_DIRECTORY   <app>/service.json format
    
  --dry-run             Preview effect of action
  
```

 ### Examples
 
 1. Clone all repositories to local disk (uses git executable)
 
 ```bash
 service-manager pull --service-directory <path to service dir> --vcs-user <user name> --vcs-password <pass> --vcs-root-url <url>
 ``` 
 2. List all services
 
 ```bash
 service-manager list --service-directory <path to service dir> --vcs-user <user name> --vcs-password <pass> --vcs-root-url <url>
 ```
 3. Inspect all services and create any that are not existing in git
 
 ```bash
 service-manager sync --service-directory <path to service dir> --vcs-user <user name> --vcs-password <pass> --vcs-root-url <url>
 ```
 
  
