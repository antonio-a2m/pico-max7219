import json
import subprocess

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

   def read(self):
      try:
         with subprocess.Popen(["rshell","--quiet","cat","/pyboard/content.json"], 
                              stdout=subprocess.PIPE) as proc:
            json_in_pico=proc.stdout.read()
         return json.loads(json_in_pico)
      except json.decoder.JSONDecodeError: 
         return {"error":"could not access pico"}

   def write(self,data):
      temp_file_name="/tmp/content.json"
      try:
         with open(temp_file_name,"w") as outfile:
            json.dump(data,outfile)            
      except:
         print("could not write")
         return {"error":"could not access pico"}

      with subprocess.Popen(["rshell","--quiet","cp",temp_file_name,"/pyboard"], \
                           stdout=subprocess.PIPE,) as proc:
         json_in_pico=proc.stdout.read()
         print(json_in_pico)
