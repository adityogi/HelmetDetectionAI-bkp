from flask import Flask

class App():
  def __init__(self) -> None:
    self.app = Flask(__name__)

  def set_debug(self,value:bool) -> None:
    self.app.config["DEBUG"] = value

  def get_app(self):
    return self.app

  