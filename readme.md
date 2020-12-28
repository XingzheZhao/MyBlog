# MyBlog

### Table of Content

- [Description](#description)
- [Getting Started](#getting-started)
- [Run Program](#run-program)
- [Author Infor](#author-info)

---

## Description

This is a flask web application that allows users to create account, update infomation, make posts and so on.

---

## Getting Started

#### Clone

- Clone this repo to your local machine by using this link <span style="background-color:grey">https://github.com/XingzheZhao/MyBlog.git</span>

```bash
git clone https://github.com/XingzheZhao/MyBlog.git
```

#### Installation Setup

- The following instructions are for Windows users. If you are running on MacOS or Linux, you can simply use pip3 and python3 instead of pip and python.
- Even though requirements.txt file is included, installing each required package manually is recommended. Alternatively, you can run the command below and install missing package additionally.

```bash
pip install -r requirements.txt
```

- Make sure your Python version is Python 3.9

```bash
pip install flask
```

```bash
pip install wtf-form
```

```bash
pip install Flask-Mail
```

```bash
pip install Flask-Login
```

```bash
pip install pillow
```

```bash
pip install SQLAlchemy
```

```bash
pi install -U python-dotenv
```

```bash
pip install Flask-MySQLdb
```

```bash
pip install mysqlclient-1.4.6-cp39-cp39-win_amd64.whl
```

#### Environmental Variable Setup

- In order to run the program, environmental variables are needed to be set separately.
- Creates a .env file in your working directory.
- In your .env file, gives the required environmental variables (total of 7 variables) the proper values like this format

  > MYSQL_HOST = "localhost"

  > MYSQL_USER = "root"

  > MYSQL_PASSWORD = "your_password"

  > MYSQL_DB = "your_db"

  > APP_SECRET_KEY = "SECRET"

  > EMAIL_USER = "user@demo.com"

  > EMAIL_PASS = "password"

---

## Run Program

- Open your terminal or command prompt, go to the run.py directory and excute the program by using the following command

```bash
python run.py
```

[Back To The Top](#myblog)

---

## Author Info

- Linkedin - [Xingzhe (Sam) Zhao](www.linkedin.com/in/sam-xingzhe-zhao-ab61a1112)

[Back To The Top](#myblog)
