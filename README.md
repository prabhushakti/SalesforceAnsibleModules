# Salesforce Configuration Management with Ansible!!!
![Demo Gif Video](https://github.com/prabhushakti/SalesforceAnsibleModules/blob/dev/assets/demo.gif)

# Disclosure
This is an unofficial Salesforce repository containing collections of modules and roles to enforce declaraitive way of developing in the platform.
This collection is not affiliated with or endorsed by Salesforce (a registered trademark of Salesforce, Inc).

# About
This is repository contains Ansible Modules and a Role for package based development. This is extremely helpful for local developments. Instead of using SFDX/SF commands/IDE-plugins: wasting time copy-pasting, reading command documentations, going back-and-forth between windows, you have a self-documenting configuration file to create packages. You don't need to search or learn any commands or tools. Just fill what you need and it gets things done.

## System requirements:
-   Requires Python 3+ 
-   Requires python ansible package

## Get Started:
_Please wait for the release. It's under development._
### Installation
- You can install this as a collection ```$ ansible-galaxy collection install salesforcedx```
- You can also manually download the releases, uncompress in /usr/share/ansible/collections/ directory.
### Quick Start
- Populate development requirements in ```vars/main.yml``` file, i.e. name of project, package you're building, version etc.
- Create/Recreate the development enviornment, scratch org, package, deploy, test in one command: 
``` $ ansible feature_WI123X.yml --tags "createProject, createScratchORG, createPackage, deployPackage"``` 
- Create a scratch org imperatively: 
``` $ ansible feature_WI123X.yml --tags createScratchORG -e  "orgName: testWI007"```



