#!/usr/bin/python
import argparse

def login(args):
    import pdb; pdb.set_trace()
    print(args)

def commandline():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', default='1')
    subparsers = parser.add_subparsers(title='subcommands',  
                                       description='valid subcommands',  
                                       help='additional help',  
                                       dest='subparser_name')  
  
    parser_foo = subparsers.add_parser('login')  
    parser_foo.add_argument('-u','--username' , default='root')  
    parser_foo.add_argument('-p', '--password', default='nls72NSN')
    parser_foo.set_defaults(func=login)
    parser.parse_args()

if __name__=='__main__':
    commandline()
