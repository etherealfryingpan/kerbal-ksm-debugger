from cx_Freeze import setup, Executable

setup(name='ksm_debugger',
      version='0.1.0',
      packages=['ksm_debugger'],
      executables = [Executable('ksm_debugger\\__main__.py', targetName='ksm_debugger.exe')]
      )