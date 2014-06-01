py-txt2fb2
==========

New version of txt to FictionBook converter.

Pictures (JPG, PNG, GIF) in plain text for example:
    <imagename.jpg>

## Files

titlematcher.py - regular expressions for matching new title or chapter. (Attention: Please, change it for you book! Or document may be invalid.)  
tokenlist.py - regular expressions for tokenize text. (Change it, if you want to add pictures.)  
main.py - main file for project.  

## Requirement

Python 3.4  
PIL or PILLOW for convert images  

## Using

Call main.py with arguments. For help:
    python3 main.py -h