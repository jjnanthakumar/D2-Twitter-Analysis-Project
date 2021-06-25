Deploying Django app on Heroku with GitHub
==========================================



![](https://miro.medium.com/max/2018/1*RKww7E3bI2YKr1Mww62skw.png)

Heroku provides many powerful features for deploying a project up on a live server to access it from anywhere in the world. The easiest way is to integrate it with GitHub and deploy code living on GitHub. Heroku can automatically build and release (if the build is successful) pushes to the specified GitHub repository.

**_Prerequisites_** : GitHub Account and Django App.

Here is the list of things we would be doing-

*   _Create an app on Heroku_
*   _Prepare the app for deployment_
*   _Push code to GitHub_
*   _Deploy on Heroku_

Lets get started!

1\. Sign up and create an app on Heroku
---------------------------------------

Sign up for a free heroku account by entering your details [here](https://signup.heroku.com/).

Login to your account and click on New> **Create new app**.

<img src="https://github.com/jjnanthakumar/D2-Twitter-Analysis-Project/blob/main/media/img1.jpg?raw=true" width="auto" height="auto" sizes="800px" role="presentation"/>

Enter a unique App name. (it might take a few tries sometimes to see what’s available). Check region and click on Create app.


2\. Preparing Django App for deployment
---------------------------------------

Preparing Django App for deployment consists of adding a few files to project root directory, installing few packages and configuring the settings.py file for heroku deployment. Dive right in and follow the steps-

In Django settings.py, set debug value to False and in **ALLOWED\_HOSTS**, enter your heroku app domain name that we just created above.

```
DEBUG = False
ALLOWED_HOSTS = ['<appname>.herokuapp.com']
```

Next, install the below packages-

```
pip install gunicorn  
pip install whitenoise
```

**Gunicorn** is a Python-HTTP server for WSGI applications and **WhiteNoise** allows our web app to serve its own static files. Now in your project settings.py add **‘whitenoise.middleware.WhiteNoiseMiddleware’,** in the MIDDLEWARE section as shown below-

<img alt="" class="t u v jo aj" src="https://github.com/jjnanthakumar/D2-Twitter-Analysis-Project/blob/main/media/img2.jpg?raw=true" width="auto" height="auto" sizes="700px" role="presentation"/>

As Heroku doesn't serve static files, we need to configure **STATIC\_ROOT** in our project settings.py file by adding the below line above our static\_url

<img alt="" class="t u v jo aj" src="https://github.com/jjnanthakumar/D2-Twitter-Analysis-Project/blob/main/media/img3.jpg?raw=true" width="auto" height="auto" sizes="700px" role="presentation"/>

Next, create a file called “**Procfile**” without any file extension in your app’s root directory(which contains manage.py). It specifies the commands that are executed by the app on startup. Here, we specify a process type by adding the below line in the file

```
web: gunicorn projectname.wsgi --log-file -
```

Note: project name should be the name of the folder containing the wsgi file, settings.py file

Next, create a file **runtime.txt** in django project root directory(where manage.py file is present). This tells Heroku what version of python we are using. Enter the version of python you are using in the file.

<img alt="" class="t u v jo aj" src="https://github.com/jjnanthakumar/D2-Twitter-Analysis-Project/blob/main/media/img4.jpg?raw=true" width="auto" height="auto" sizes="700px" role="presentation"/>
Now, run the below command in the terminal

```
pip freeze > requirements.txt
```

This creates a **requirements.txt** file in the root directory(same as that containing manage.py file) and the file contains the list of all packages and their versions that are needed to make the project work. All the dependencies specified in the file are automatically installed before the app startup in heroku.(If you install new packages and run the same command, it would update the existing file)

This concludes the project settings and next we will push the code to GitHub and deploy it.

3\. Push the code to GitHub
---------------------------

I used the VisualStudio IDE and created a private repository and pushed my code to GitHub. For this, in the menu bar navigate to Source Control> Import into Version Control> Share project on GitHub. Enter a repository name , check on private and Share. See details [here](https://code.visualstudio.com/docs/editor/github).

Another alternative is, Create an empty private repository in your GitHub account. Drag and drop the files (leaving the virtual environment ENV folder) from your project folder to the repo directly and commit them to the master branch.

If you have an existing repo, then push the latest code and merge it to the master branch, as we would be deploying the master branch itself.

4\. Deployment in Heroku
------------------------

In Heroku, navigate to your app> Settings. Scroll down and click on **Add buildpack**\> Select Python > Save changes

<img alt="" class="t u v jo aj" src="https://github.com/jjnanthakumar/D2-Twitter-Analysis-Project/blob/main/media/img4.jpg?raw=true" width="auto" height="auto" sizes="700px" role="presentation"/>

Navigate to Deploy tab, under Deployment method> click on GitHub. Click on **Connect to GitHub** button below. A pop up appears asking for authorization to connect to your GitHub account. Click on Authorize Heroku. In the Connect to GitHub section, search for your repository. Click on Connect.

<img alt="" class="t u v jo aj" src="https://github.com/jjnanthakumar/D2-Twitter-Analysis-Project/blob/main/media/img5.jpg?raw=true" width="auto" height="auto" sizes="700px" role="presentation"/>

Once connected, you have options to deploy it Manually or Automatically. With manual deploys, you can create an immediate deployment of any branch from the connected repository. Use manual deploys if you want to control when changes are deployed to Heroku.

Automatic deploy can be used, if you want to deploy every time a new push is made to master. When you enable automatic deploys for a branch, Heroku builds and deploys all pushes made to that branch automatically.

Select the branch (master) and click on **Deploy Branch**. This starts the build process and once done, a success message is displayed.

Click on the **View** button. This should launch your app in the browser, Your app is now up, live and running and can be accessed from anywhere around the world, Congratulations !



![](https://miro.medium.com/max/6912/0*zdyWnOEHPQlpo0Mw)Photo by [Ben Kolde](https://unsplash.com/@benkolde?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)