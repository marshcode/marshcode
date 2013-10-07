#enable flask debug mode.  If this is active, the python logging system will not be configured
DEBUG=False

#Log file containing warnings and above.  It is reccomended that this be an absolute path in the second config file
ERROR_LOG_FILE = "davesite.error.log"

#Nested list with entries of the format ('Heading', 'http://www.the_url.com') or
#('Menu Heading', [('Heading1', 'URL1'), ('Heading2', 'URL2')])
MENU = [('a', '/b')]                               
                                                                              
#Script location on the server (relative to the root).  Use this to adjust the prefix created by flask.url_for
SCRIPT_NAME='/'                            