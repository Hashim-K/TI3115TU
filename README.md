# TI3115TU Template Repository

Welcome developers. After reading the Brightspace manual on setting up your computer for Gitlab. This is the last document you'll need to read to setup/configure your project.

## Setup / Configuration
* Preliminaries: Have Python 3, Git Bash & Pycharm (EDU or Community) installed
* You'll use PyCharm to clone your central repository directly into a local repository in the PyCharm working directory.
* The TAs ran a couple of different installation/configuration options, but they are by no means exhaustive. 
* If you run into problems, ask a TA. They are happy to help!

### For PyCharm EDU/Windows:
* run PyCharm Education
* Select `VCS` > `Check out from Version Control` > `Git` > enter your project GitLab project URL
* `Would you like to open the directory?` > `Yes`
* A couple of configurations once you're inside:
    * Go to `File` > `Settings` > `Project` > `Project Interpreter` > `Show all` > `Add (+)` > `Virtualenv Environment` > Select a version of Python as `Base Interpreter` > `OK` (3 times)
    * Go to `File` > `Settings` > `Tools` > `Python Integrated Tools` and change the default test runner to be `pytest`
    * Open `requirements.txt`, and in the yellow popup that appears, click on `Install requirements`
    * You can also install the requirements through the Terminal by running the following command:
    ```
    pip install -r requirements.txt
    ```
  
### For PyCharm Community/Windows:  
* run PyCharm Community
* Click on `Get from Version Control`
* On the next screen select all defaults should be selected already, but if not:  
  `Repository URL` on the left  
  `Version control: Git` on the right  
  copy and paste you SSH Git URL from your project main page into the `URL` field:
  `git@gitlab.ewi.tudelft.nl:ti3115tu/2020-2021/group-XX.git` (where XX is your group number)  
  
Pycharm will now clone your group repository into its project folder. While PyCharm is setting up some stuff, you still need to configure some settings for your project.

* Go to `File` > `Settings` > `Project: group-XX`. Select `Python Interpreter` on the right   
and click the gear icon in the top right > `Show all` > `Add (+)` > `Virtualenv Environment` > 'OK' (twice)  
 This creates a virtual environment for your Python project; it's an isolated workspace for your Python project in which you can install dependencies locally, without cluttering your system.
* Next in the same `File` > `Settings` > `Tools` > `Python Integrated Tools` change the default test runner to be `pytest` and hit 'OK' (if you get a warning `No pytest runner found in selecter interpreter` ignore it, you'll be installing pytest in a bit anyway)
* Last thing todo is install some dependencies for your project in PyCharm. Open `requirements.txt` in your root project folder, and click `ignore extension` if you see a message in yellow/black: `Plugins supporting requirements.txt files found`
Why? It would install a 3rd party plugin, but we'll install the plugins in just a bit ourselves. 
* Open a terminal window from within Pycharm.  
Enter `pip install -r requirements.txt`, hit `[enter]` et voila, your dependencies will install automatically.

### For PyCharm EDU/MAC OS X:
* run PyCharm EDU
* Click on `Get from Version Control`
* Go to `PyCharm` > `Preferences` > `Project: <project_name>` > `Python Interpreter` > Click on the drop-down menu > `Show all...` > `Add (+)` > `Virtualenv Environment` > Select a version of Python as Base Interpreter > `OK` (3 times)"
* Go to `PyCharm` > `Preferences` > `Tools` > `Python Integrated Tools` and change the default test runner to be `pytest` (ignore the fix button/message popping up: you'll install pytest in a bit anyway).
* Last thing todo is install some dependencies for your project in PyCharm. Open `requirements.txt` in your root project folder, and click `ignore extension` if you see a message in yellow/black: `Plugins supporting requirements.txt files found`
Why? It would install a 3rd party plugin, but we'll install the plugins in just a bit ourselves. 
* Open a terminal window from within Pycharm.  
Enter `pip install -r requirements.txt`, hit `[enter]` et voila, your dependencies will install automatically.

### For PyCharm Community/MAC OS X:
We didn't test drive this guide for this specific setup. Checking the above sections should give you enough information to figure out how to configure Gitlab with PyCharm Community for your OS. 
If not, then again: TAs are happy to help :).

### For Linux users:
Linux is the awesome. When you have this running the sky clears up. You don't need help.(obviously \*duh\*). But in case you do: consult the TAs. They're happy to help.

## Orientation of the project files in PyCharm
You're now done setting up PyCharm/Gitlab. Yeuj! :) Good. You can start developing your project asap. You'll meet weekly from now on with one of your assigned TAs and he/she will be your guide for the whole project.
Best of luck in developing your final product! The next sections describe the project structure, how to start the example program, run tests on it and check coverage + coding violations.

### On the Structure
* `docs` contains your project documentation (e.g. your planning meetings, but also any diagrams or requirements documents you would like to keep track of centrally).
* `project` contains mAost Python source files and tests. For now we have provided a sample Python program with some example tests.
* **DO NOT change the ```project``` directory name. Otherwise, you will get FAILING builds in your CI.**
### Running 
Run the sample code by right-clicking on `project/factorial_calc.py` and selecting `Run`.

### Testing
To run all tests, right-click on the `project/test` folder and select `Run 'pytest in test'`. To run an individual test, click on the green play button next to it.
You can also do the same through the terminal (open it in PyCharm by clicking on `Terminal` in the lower toolbar - you may have to click on the icon in the bottom-left corner to reveal it):
```
pytest project
```

### Coverage
For only a quick check coverage check you can also enter the following two commands.  
The first records coverage while running PyTest and the second one shows it in your terminal:
```
coverage run -m pytest project
coverage report
```

Do you want to generate documentation of the coverage? Run the following command (from within the PyCharm terminal):
```
pytest --cov-config=.coveragerc --cov=project --cov-report=html project/test
```
The output goes into the `htmlcov` directory. You can view your coverage report by right-clicking on the `index.html` file in that directory and selecting `Open in Browser`!

## Pylint
Run `pylint` to check for coding style violations by running the following command (from within the PyCharm terminal):
We have deliberately put in some flaws for you to check the output of PyLint.
```
pylint project
```