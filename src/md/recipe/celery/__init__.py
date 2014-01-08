import logging
import os
import shutil
import zc.buildout
import zc.recipe.egg


LOADER_TEMPLATE = """
import loader

def zope_loader(app):
    return loader.ZopeLoader(
        app,
        celery_conf='{celery_conf}',
        zope_conf='{zope_conf}')
"""

INIT_TEMPLATE = """
import logging.config
import sys

# Initialize logging as early as possible
logging.config.fileConfig('{logging_conf}')

# Check if user defined a loader, then he is on his own
if not any(['--loader=' in s for s in sys.argv]):
    sys.argv.append('--loader=zopeloader.zope_loader')
else:
    print "Using custom loader"
"""


class Recipe(object):

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options

        options.setdefault(
            'config-path',
            os.path.join(self.buildout['buildout']['parts-directory'],
            self.name))

        options['location'] = os.path.join(
            buildout['buildout']['parts-directory'],
            self.name,
        )

    def install(self):
        options = self.options
        logger = logging.getLogger(self.name)
        loader_filename_list  = []
        import pdb;pdb.set_trace()
        
        dest = options['config-path']
        if options.get('no-loader','false') != 'true':
            loader_filename = os.path.join(dest, 'zopeloader.py')

            if not os.path.exists(dest):
                logger.info('Creating directory %s.' % dest)
                os.makedirs(dest)

            baseloader_filename = os.path.join(
                os.path.dirname(__file__), 'loader.py')
            shutil.copy(baseloader_filename, dest)
            loader_file = open(loader_filename, 'w')
            loader_file.write(
                LOADER_TEMPLATE.format(
                    celery_conf=options.get('celery_conf'),
                    zope_conf=options.get('zope_conf')))
            loader_file.close()
            loader_filename_list.append(loader_fileanme)
            logger.info('Generated loader file %s.' % loader_filename)
        logger.info('Using default loader')
        if options.get('extra-paths'):
            dest += '\n' + options.get('extra-paths')
            
        celery_egg_options = {
            'eggs': 'celery',
            'extra-paths': dest,
            'initialization': INIT_TEMPLATE.format(
                logging_conf=options.get('logging_conf'))}
        if options.get('no-init','false') == 'true':
            celery_egg_options.pop('initialization')
        if 'eggs' in options:
            celery_egg_options['eggs'] = '\n'.join(['celery']
                                                   + options['eggs'].split())
        if 'scripts' in options:
            celery_egg_options['scripts'] = options['scripts']
        celery_egg = zc.recipe.egg.Egg(
            self.buildout,
            self.name,
            celery_egg_options)

        return loader_filename_list + list(celery_egg.install())

    update = install
