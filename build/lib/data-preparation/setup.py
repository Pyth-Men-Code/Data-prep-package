from numpy.distutils.misc_util import Configuration

def configuration(parent_package="", top_path=None):
  config = Configuration('data_preparation', parent_package, top_path)

  return  config

if __name__ == '__main__' :
    configuration()