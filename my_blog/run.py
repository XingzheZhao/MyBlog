from myblog import app


if __name__ == '__main__':
  app.config['TEMPLATES_AUTO_RELOAD'] = True
  app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
  app.run(debug=True)