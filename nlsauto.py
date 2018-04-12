import argparse
  
def args(*args,**kwargs):  
    def _decorator(func):  
        func.__dict__.setdefault('args', []).insert(0, (args,kwargs))  
        return func  
    return _decorator  
  
class Dbcommands(object):  
    def __init__(self):  
        pass  
 
    @args('version', nargs='?', default='versiondefault',  
            help='version help')  
    def sync(self, version=None):  
        print "do Dbcommand.sync(version=%s)." %version  
  
    def update(self):  
        print "do Dbcommand.update()."  
  
class Hostcommands(object):  
    @args('zone', nargs='?', default="zonedefault",  
            help=' zone help')  
    def list(self,zone=None):  
        print "do Hostcomands.list(zone=%s)." %zone  
  
def methods_of(obj):  
    result = []  
    for i in dir(obj):  
        if callable(getattr(obj, i)) and not i.startswith('_'):  
            result.append((i, getattr(obj, i)))  
    return result  
  
def fetch_func_args(func,matchargs):  
    fn_args = []  
    for args,kwargs in getattr(func, 'args', []):  
        arg = args[0]  
        fn_args.append(getattr(matchargs, arg))  
  
    return fn_args  
  
CATEGORIES = {  
    'db' : Dbcommands,  
    'host': Hostcommands}  
  
if __name__ == "__main__":  
    top_parser = argparse.ArgumentParser(prog='top')  
  
    subparsers = top_parser.add_subparsers()  
  
    for category in CATEGORIES:  
        command_object = CATEGORIES[category]()  
  
        category_parser = subparsers.add_parser(category)  
        category_parser.set_defaults(command_object=command_object)  
  
        category_subparsers = category_parser.add_subparsers(dest='action')  
        for (action, action_fn) in methods_of(command_object):  
            parser = category_subparsers.add_parser(action)  
  
            action_kwargs = []  
            for args, kwargs in getattr(action_fn, 'args', []):  
                parser.add_argument(*args, **kwargs)  
  
            parser.set_defaults(action_fn=action_fn)  
            parser.set_defaults(action_kwargs=action_kwargs)  
  
  
    match_args = top_parser.parse_args('db sync 3'.split())  
    print 'match_args:',match_args  
  
    fn = match_args.action_fn  
    fn_args = fetch_func_args(fn,match_args)  
  
    #do the match func  
    fn(*fn_args) 
