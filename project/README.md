![](<project/readme_files/258_logo.png>)



<h1 align="center">25/8</h1>

<h4 align="center">by Group 25</h4>

> 25/8 relieves you of all the daunting aspects of scheduling. By simply providing it with basic outlines of what you have to do and when it has to be done, 25/8 will generate your weekly schedule.



## :label: Key Features

- Google Calendar importing and exporting
- Daily routines functionality
- Extensive task specification
- Rich GUI that allows the user to effortlessly create and change tasks
- No loss of data
  - Each change will be saved to the hard disk at the moment of making it.
- Dark Mode only
- Cross Platform
  - Windows (tested)
  - macOS and Linux ready (untested)



## :package: How to Install

In order to clone and run this application, [Git](https://git-scm.com/) and a [Python 3.9.6](https://www.python.org/downloads/release/python-396/) (or newer) environment should be installed on your machine. 

To clone the application, run in the command line:

```bash
# Clone this repo
$ git clone https://gitlab.ewi.tudelft.nl/ti3115tu/2021-2022/group-25.git
```

With the clone present locally, we still have to handle the dependencies. These are listed under `/requirements.txt` in the root folder of the clone and must be installed into the virtual environment that you wish to use to run 25/8. 

## :writing_hand: How to Use

Upon opening 25/8 you will be greeted with a 'Home Window' that explains the basic steps in going from a bunch of tasks that each have their own deadline to a neat schedule that can be exported to your Google Calendar.

## :cop: Security

You should be aware of the fact that all data written by 25/8 is stored with no encryption of any kind. This includes the OAuth2 user credentials that are fetched upon connecting a Google account. We therefore advise users to employ the online functionalities at their own discretion.

