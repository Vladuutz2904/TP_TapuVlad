import argparse, json, os

path = "folder/subfolder/file/love.txt"
result = path.rsplit("/",1)[-1]
print(result)
