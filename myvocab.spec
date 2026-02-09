# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['myvocab.py'],
             pathex=['C:\\wrk\\Python\\VSC\\myvocab'],
             binaries=[],
             datas=[('.env', '.'), ('src/myvocab/parsing/infinitive/data', 'src/myvocab/parsing/infinitive/data'), ('src/myvocab/parsing/singularization/data', 'src/myvocab/parsing/singularization/data')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
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
          name='myvocab',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
