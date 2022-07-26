# service-buddy 

[![Upload Python Package](https://github.com/Nudge-Security/service-buddy/actions/workflows/python-publish.yml/badge.svg)](https://github.com/Nudge-Security/service-buddy/actions/workflows/python-publish.yml)
## Installation

```bash
pip install service-buddy
```

## Usage

```bash
Usage: service-buddy [OPTIONS] COMMAND [ARGS]...

  CLI for managing the repositories and build pipeline in a micro-service
  architecture.

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
  clone     Clone all of the existing service definition repos onto the local
            file system
  git       Run arbitrary git command for each service
  init      Analyze service definitions and initialize any new services.
  list      Print definitions for services.
  boostrap  Create a repository containing the initial definition for a micro-service stack managed by service-buddy.
```

 ### Examples
 
 1. Bootstrap your service definitions, creating an initial repository for use with service-buddy
 ```bash
 service-buddy bootstrap
 ```
 
 2. Clone all repositories to local disk (uses git executable).  Assumes your working directory is the directory created by the service-buddy bootstrap command
 
 ```bash
 service-buddy clone 
 ```
 
 
 3. Pull the latest for all repositories existing on local disk (uses git executable and requires 'clone' to be run first)
 
 ```bash
 service-buddy  git commit -m "Big old Commit"
 ``` 
 
 4. List all services
 
 ```bash
 service-buddy  list
 ```
 5. Inspect all services and create any that are not existing in git
 
 ```bash
 service-buddy  init 
 ```
 
  
