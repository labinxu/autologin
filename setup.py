from distutils.core import setup
import sys
sys.path.append('C:/msys64/usr/lib/python3.6/site-packages')
import py2exe
sys.argv.append('py2exe')
py2exe_options = {
        "compressed": 1,
        "optimize": 2,
        "ascii": 0,
        "bundle_files": 1,}# 其中bundle_files有效值为：
                                  # 3 (默认)不打包。
                                  # 2 打包，但不打包Python解释器。
                                  # 1 打包，包括Python解释器。
setup(
      name = 'console demo',
      version = '1.0',
      console = ['wifipwd_dispatcher.py',],
      zipfile = None,
      options = {'py2exe': py2exe_options}
      )

