# Note SYMS require central python installation via platform package manager 
# eg. sudo apt-get install python-lxml2 (or config management, eg. BCfg2) 
# Must also install Fabric and virtualenv in this manner first

SITEPGS = 'lib/python2.6/site-packages'
SCRAPYSYMS = ['/usr/share/pyshared/libxml2.py',] # python-lxml2
SCRAPY = ['twisted', 'pyopenssl', 'Scrapy']

def scrapybuild(site='localhost', dir='scrapy', bare=True):
    """ fab:site,dir,bare Install scrapy via virtualenv """
    with settings(host_string=SITES[site]):
        folder = os.getcwd()
        with cd(folder):
            if bare:
                run('virtualenv --no-site-packages %s' % dir)
            else:
                run('virtualenv %s' % dir)                
        folder = os.path.join(folder, dir)
        with cd(os.path.join(folder, SITEPGS)):
            for link in SCRAPYSYMS:
                if not files.exists(link):
                    run('ln -s %s' % link)
        with cd(folder):
            for egg in SCRAPY:
                run('bin/pip install %s' % egg)

def cookieaudit(site='localhost', dir='scrapy', bare=True):
    """ install cookie audit for scrapy """
    scrapybuild(site, dir, bare)
    with settings(host_string=SITES[site]):
        with cd(dir):
            run('git clone https://github.com/edcrewe/cookie_audit uob')
