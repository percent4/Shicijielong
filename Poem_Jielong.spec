# -*- mode: python -*-

block_cipher = None


a = Analysis(['Poem_Jielong.py'],
             pathex=['G:\\ʫ�ʽ���'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Poem_Jielong',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
