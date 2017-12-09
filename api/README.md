TODO: write the readme!
# Corp-HQ API
This project is designed to be the backing API of the 
[Corp HQ UI](https://github.com/fritogotlayed/corp-hq-ui).
This project uses [Trello](https://trello.com/b/YLDkKjjj/corp-hq) to track
in-flight work.

## Mission
Create web based, single source set of tools to enhance Eve Online gameplay for
small and medium size corporations. 


## To Contribute
When planning on contributing to the either project in the Corp-HQ application
please fork the repo and PR your changes accordingly. If your chane affects
both projects include links to the PR in the other projects. This enables
reviewers to pull all changes related to your bug fix / feature locally for
testing.

### Local Environment Getting Started
* `make create-venv`
* `source .venv/bin/activate`
* `make dev-install`

There is a `developer.py` located at the root of the project. This file is
intended for devs to run the application locally. Please be careful when PR-ing
this file. Likewise, if you have modifications you may wish to stash them
locally.

## Configuration
In an effort to make this application as configurable as possible while still
maintaining the flexibility of Docker application configuration will be kept in
the database. For items that cannot be stored in the database, such as the 
connection details, these items will be provided to the application via environment
variables. For now the only database that is supported is mongo. If this changes
for whatever and storing the configuration document in the database is no longer
an option a grace period will be communicated in this readme.

* Current Config Grade Period Ends: N/A

### Contribution Checklist
* Ran `make test` and all was successful
* Ran `make pretty`
* PR made using PR template
  * TODO: Create / link template

## Dependencies
### External
* [Mongo Database](https://www.mongodb.com/)
* [Eve API](https://esi.tech.ccp.is/latest/)