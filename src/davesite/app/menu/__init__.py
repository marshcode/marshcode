import collections

def read_menu():
    
    web_projects = dict()
    web_projects['Jean-Luc Picard Advisor'] = '/jlp/'
    
    d = collections.OrderedDict()
    d['Home'] = '/'
    d['Web Projects'] = web_projects
    d['Projects'] = '/projects/'
    d['Related Sites'] = dict(Trac = 'https://trac.davemarsh.webfactional.com/',
                              SVN = 'https://svn.davemarsh.webfactional.com/')
    
    return d