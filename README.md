# service-manager

[Build Status](https://api.travis-ci.org/AlienVault-Engineering/service-manager.png) 
## Installation

```bash
pip install service-manager
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
    
  --service-directory   Directory containing service definitions in
    SERVICE_DIRECTORY   <app>/service.json format
    
  --dry-run             Preview effect of action
  
```

 ### Examples
 
 1. Clone all repositories to local disk (uses git executable)
 
 ```bash
 service-manager  --service-directory <path to service dir>  pull --destination-directory .
 ``` 
 2. List all services
 
 ```bash
 service-manager  --service-directory <path to service dir> list
 ```
 3. Inspect all services and create any that are not existing in git
 
 ```bash
 service-manager  --service-directory <path to service dir> sync --destination-directory .  --service-template-definitions
 ```
 
  
