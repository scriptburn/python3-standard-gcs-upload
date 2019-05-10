from google.appengine.ext import vendor
import os

# Third-party libraries are stored in "lib", vendoring will make
# sure that they are importable by the application.
if os.path.isdir(os.path.join(os.getcwd(), 'env/lib/python2.7/site-packages')):
    vendor.add('env/lib/python2.7/site-packages')