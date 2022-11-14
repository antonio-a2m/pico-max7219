import json
from lib import pyboard

class LocalFile:

   def __init__(self,filename) :
      self.filename = filename

   def read(self):
      try:
         with open(self.filename,"r") as infile:
            return json.load(infile)
      except FileNotFoundError: 
         return {"displays":[]}
      except json.decoder.JSONDecodeError: 
         return {"error":"could not access local file"}

   def write(self,data):
      try:
         with open(self.filename,"w") as outfile:
            json.dump(data,outfile)            
      except:
         print("could not write")
         return {"error":"could not access localfile"}

class Pico:
   def do(self,action):

      cmds={
         "read": ["cp",":content.json","content.json"],
         "write":["cp","content.json",":content.json"]
      }
      pyb = pyboard.Pyboard('/dev/ttyACM0')
      pyb.enter_raw_repl()
      pyboard.filesystem_command(pyb,cmds[action])
      pyb.exit_raw_repl()
      pyb.close()

   def read(self):
      try:
         self.do("read")
         with open ("content.json","r") as localfile:
            json_in_pico=localfile.read()
         return json.loads(json_in_pico)
      except json.decoder.JSONDecodeError: 
         return {"error":"could not access pico"}
      except :
         print("os error")
         return {"displays": [{"text": "hello amigos", "effect": "blink"}]}

   def write(self,data):
      temp_file_name="content.json"
      try:
         with open(temp_file_name,"w") as outfile:
            json.dump(data,outfile)
         self.do("write")
      except:
         print("could not write local")
         return {"error":"could not access pico"}

      
