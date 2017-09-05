# service-buddy

[Build Status](https://api.travis-ci.org/AlienVault-Engineering/service-manager.png) 
## Installation

```bash
pip install service-buddy
```

## Usage

```bash
Usage: service-buddy [OPTIONS] COMMAND [ARGS]...

  CLI for managing the repositories and build pipeline in a micro-service
  architecture..

Options:
  --application-filter TEXT     Constrain command to operate on applications
                                that match the passed filter
  --service-directory PATH      Directory containing service definitions in
                                <app>/service.json format.  Default is
                                './services'
  --destination-directory PATH  The directory where the repositories for each
                                service should be created or currently exist.
                                Default is './code'
  --verbose                     Print verbose status messages
  --dry-run                     Preview effect of action
  --help                        Show this message and exit.

Commands:
  clone  Clone all of the existing service definition repos onto the local
         file system
  git    Run arbitrary git command for each service
  init   Analyze service definitions and initialize any new services.
  list   Print definitions for services.
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
 
  
