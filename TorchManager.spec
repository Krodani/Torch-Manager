# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None


a = Analysis(['TorchManager.py'],
             pathex=[os.getcwd()],
             binaries=[],
             datas=[('./TorchManager.ui', '.'),('./repository/*.png', 'repository'),('./repository/icon.ico', 'repository'),('./about.ui', '.'),('./repository/minecraft_click.wav', 'repository')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='TorchManager',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
		  onefile=True,
          console=False,
		  icon='repository/icon.ico')
