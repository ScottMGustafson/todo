#! /usr/bin/env python
"""
a simple todo list script:
=================================

setting it up:
---------------------------------
--put the script somewhere and make the appropriate changes to ~/.bashrc.    For 
    example, one may want to add this to ~/.bashrc:

        function todofunction {
            TODOPATH="/home/scott/bin/"
            $TODOPATH'todo.py' "$@"
        }

        alias todo=todofunction

--change the values of 'location' and 'name' in todo.cfg to fit your system and 
    preferences.    'name' determines the name of the todo list and 'location' 
    determines its location.

--todo.cfg should always be in the same directory as todo.py

running:
-------------------------------
--run on the command line like:
    > todo.py <command> <text>
    
    examples:
    >    todo.py add 2:do something
    will place write 
    "2     : do something"
    in todo.txt on the second line
    
    >    todo.py add do something
    will put the same text, but in the first place

    > todo.py    list
    will print out the todo list by calling 'more <name> | less'

    > todo.py done    3
    will remove the third item on the list

    

"""

import os
import sys

class Item(object):
    """an item of the todo list"""
    def __init__(self,priority=1,text=''):
        self.text = text
        try:
            self.priority = int(priority)
        except ValueError:
            print("priority must be an integer:    "+str(priority))
            sys.exit()
        except:
            raise
        
    def __str__(self):
        return ("%-4d: %s")%(self.priority,self.text)


class Todo(object):
    """the todo list class"""
    def __init__(self):
        location, name = self.configure()
        if location[-1]!='/':    
            location+='/'
        self.name = location+name
        self.data = []
        self.rawText = []
        self.data, self.rawText = self.retrieve()

# raw text is kept as is and not altered

    def configure(self):
        """configure the todo list."""
        configfile = os.path.dirname(os.path.abspath(__file__))+'/todo.cfg'
        try:
            f = open(configfile,'r')
        except IOError:
            print('configuration file does not exist.')
            sys.exit()

        cfg_dict = {}
        for line in getNonBlank(f):
            data = line.split(':')
            if len(data)!=2:
                print('configuration file in wrong format.    should be: \n    key : value ')
                sys.exit()
            else:
                cfg_dict[data[0].strip()] = data[1].strip()
        try:
            location = cfg_dict['location']
        except KeyError:
            print('key: \'location\' does not exist.')

        try:
            name = cfg_dict['name']
        except KeyError:
            print('key: \'name\' does not exist.')
        except:
            raise
        return location, name
            
    def parseItem(self,string):
        """
        parse a string to harvest an Item instance.
        """

        if string is None:
            return

        string = string.strip()
        try:
            num,text = string.split(':') 
            num = int(num.strip())
            text = text.strip()
            return Item(num,text)
        except:
            return Item(1,string)     

#    def autoSort(self):
#        self.data = sorted(self.data,key = lambda item:item.priority)

    def add(self,string=None):
        """
        insert an item into the list.    if priority is greater than list length,
        priority becomes list length.    
        """

        if string is None:
            string = raw_input("enter a task: ")
            string = string.strip()
            try:
                priority=int(raw_input("priority? (default: 1): "))
            except ValueError:
                priority = 1
            except:
                raise
            item = Item(priority,string) 
        else:
            string = string.strip()

        item = self.parseItem(string) 
        if item.priority >= len(self.data):
            item.priority    = len(self.data)+1
            index = len(self.data)
            self.data.append(item)
        else:
            index = item.priority-1
            self.data.insert(index,item)
            for i in range(index,len(self.data)):
                self.data[i].priority = i+1
        return
                
    def done(self,priority):
        """
        remove an item that has been completed, or is no longer needed.
        """
        try:
            index = int(priority) - 1
        except ValueError:
            print("priority must be an integer.")
            return
        except:
            raise

        if index>len(self.data)-1:
            print('item not found')
            return

        del(self.data[index]) 

        for i in range(index,len(self.data)):
            self.data[i].priority=i+1
        return
                     
    def retrieve(self):
        """
        open file, return list Item instances.
        if file doesn't exist, creates it.
        """
        data = []
        rawText = []
        try:
            f=open(self.name)
        except IOError:
            cmd = 'touch '+self.name
            os.system(cmd)
            return [], []

        for line in f:
            item = self.parseItem(line)
            if isinstance(item,str):            
                rawText.append(line)
            else:
                data.append(item)
        f.close()
        return data, rawText

    def writeOut(self):
        """
        write out the list
        """
        with open(self.name,'w') as f:
            for item in self.data:
                f.write(str(item)+'\n')
            for item in self.rawText:
                f.write(str(item)+'\n')
        f.close()
        return 

    def printOut(self):
        cmd = 'more '+self.name+' | less'
        os.system(cmd)
        return
        
    
def getNonBlank(filestream):
    """return lines which are neither empty, nor contain any # symbols"""
    for line in filestream:
        lines = line.rstrip()
        if lines and lines[0]!='#':
            yield lines 

commands = ['done','rm','add','list']

if __name__ == '__main__':

    try:
        cmd = sys.argv[1]
    except IndexError:
        print('need some more input')
        sys.exit()
    except: raise

    if len(sys.argv) == 2:
        if not (sys.argv[1] in commands[1:]):
            print('unrecognized command: '+sys.argv[1])
        else:
            todo = Todo()
            if cmd=='list': todo.printOut()
            else: 
                todo.add()
                todo.writeOut()

    else: # len(sys.argv>2)
        todo = Todo()
        string = ''
        for i in range(2,len(sys.argv)): 
            string+=sys.argv[i]+' '
        if cmd=='list': 
            todo.printOut()
        elif cmd=='add':    
            todo.add(string)
            todo.writeOut()
            #todo.printOut()
        elif cmd=='done' or cmd=='rm': 
            todo.done(string)
            todo.writeOut()
    return
