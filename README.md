# Database Project 

## Repo for UF Database project

### Group Members: 
* Alan Liou
* Matt Diller
* Dharani Balasubramanian
* Mohamad Ahmadzade

### Summary 
TBD

### Instructions 
- Install python3
- Install django
- Install Oracle Client libraries 
- Create local_settings.py in dbProject/ for environment variables and database connections

### Git Instructions
- Ready to start working?
    - git checkout -b <branch_name>
    - (done working)
    - git status (to see changes)
    - git add .
    - git commit -m '<message here, make it short but informative>'
    - git checkout master
    - git pull origin master
    - git checkout <branch_name>
    - git merge master 
    - git checkout master 
    - git merge <branch_name>
    - git push origin master 

- Can't get stuff to work need to go back to last commit?
    - make sure you are on your working branch
    - git reset --hard

- Alway git pull origin master to see if there are any updates

### TODO
- [ ] Users
    - [ ] Show Users
    - [ ] Create, delete and update users 
    - [ ] Add past queries to users
    - [ ] Show all past queries to users 
    - [ ] Create and design user homepage
    - [ ] Testing

- [ ] Visualization
    - [x] messages pop ontop of page (AL)
    - [X] Graphs/Tables for National Avg query (AL)
    - [X] Graphs/Tables for Time query (AL)
    - [X] Graphs/Tables for Top 10 query (AL)
    - [x] Graphs/Tables for Indicator query (AL)
    - [X] Graphs/Tables for Location query (AL)
    - [ ] Add titles
    - [ ] limit the # of entries in graphs?

- [x] Bugs
    - [x] Indicator query bug, year end query is not correct return all possible years
    - [x] top 10 query bug, does not return the specific populations, return all possible populations
    - [x] query4 topics doesn't return specified indicators
    - [x] Indicator query needs to be tweaked to return the relevant fields (MD)

- [ ] Special Features
    - [X] able to download csv file    

- [ ] Homepage/Index
    - [x] Dynamic query set up
    - [ ] create popup modals to show the options 
    - [ ] UI design done 
    - [x] Able to populate table
    - [ ] Able to combine inputs but users (what is this?)
    - [ ] Testing

