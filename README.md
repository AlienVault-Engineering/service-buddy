# service-buddy

[Build Status](https://api.travis-ci.org/AlienVault-Engineering/service-manager.png) 
## Installation

```bash
pip install service-buddy
```

## Usage

```bash
Utility to help manage microservices.

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
    
  --service-directory   Directory containing service definitions in
    SERVICE_DIRECTORY   <app>/service.json format
    
  --dry-run             Preview effect of action
  
```

 ### Examples
 
 1. Clone all repositories to local disk (uses git executable)
 
 ```bash
 service-buddy  --service-directory <path to service dir>  clone --destination-directory .
 ```
 
 
 2. Pull the latest for all repositories existing on local disk (uses git executable and requires 'clone' to be run first)
 
 ```bash
 service-buddy  --service-directory <path to service dir>  git --destination-directory <path to existing repo structure> commit -m "Big old Commit"
 ``` 
 
 3. List all services
 
 ```bash
 service-buddy  --service-directory <path to service dir> list
 ```
 4. Inspect all services and create any that are not existing in git
 
 ```bash
 service-buddy  --service-directory <path to service dir> init --destination-directory .  --service-template-definitions
 ```
 
  
