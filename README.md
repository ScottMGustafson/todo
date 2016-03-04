# todo
======

A simple command-line todo list

Setting it up:
--------------
* put the script somewhere and make the appropriate changes to ~/.bashrc.    For 
  example, one may want to add this to ~/.bashrc:

        function todofunction {
            TODOPATH="/home/scott/bin/"
            $TODOPATH'todo.py' "$@"
        }

        alias todo=todofunction

* change the values of 'location' and 'name' in todo.cfg to fit your system and 
  preferences.    'name' determines the name of the todo list and 'location' 
  determines its location.

* `todo.cfg` should always be in the same directory as todo.py

How to run:
-----------
commands are generally of the format:

        $ todo <command> <text>
    
to add something we do

        $ todo add 2:do something

which will place write 
"2     : do something"
in todo.txt on the second line
    
`$ todo` add do something
will put the same text, but in the first place

        $ todo list

will print out the todo list by calling 'more <name> | less'

        $ todo done 3

will remove the third item on the list

