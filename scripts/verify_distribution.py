# SPDX-License-Identifier: GPL-3.0-or-later
"""Review exact publication inputs. This host check is not Blender acceptance."""
import argparse,hashlib,json,re,zipfile
from pathlib import Path

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def export_files(root):
    names=json.loads((root/'docs/export-files.json').read_text(encoding='utf-8-sig'))['files']
    if not names or len(names)!=len(set(names)):raise ValueError('Empty/duplicate publication inventory')
    selected=[]
    allowed_roots={'.gitattributes','.gitignore','LICENSE','README.md','README.zh-CN.md','blenderctl.ps1'}
    allowed_dirs={'tools','docs','examples','scripts','skills','.github'}
    for name in names:
        if not isinstance(name,str) or '\\' in name or ':' in name:raise ValueError('Relative POSIX paths required')
        p=Path(name)
        if p.is_absolute() or '..' in p.parts or set(p.parts)&{'.git','runtime','dist','__pycache__','.venv'}:raise ValueError('Unsafe path: '+name)
        if name not in allowed_roots and (len(p.parts)<2 or p.parts[0] not in allowed_dirs):raise ValueError('Outside publication source families: '+name)
        if any(part.casefold().startswith(('.env','config.local')) or part.casefold()=='secrets.json' for part in p.parts):raise ValueError('Local configuration excluded')
        path=root/p
        for item in (path,*path.parents):
            if item==root.parent:break
            if item.is_symlink() or item.is_junction():raise ValueError('Links/junctions excluded')
        if not path.is_file() or not path.resolve().is_relative_to(root.resolve()):raise ValueError('Missing/escaped source: '+name)
        selected.append(path)
    return selected
def verify(root,extension=None):
    files=export_files(root);identity=json.loads((root/'docs/runtime-identity.json').read_text(encoding='utf-8-sig'))
    actual=sorted(p.relative_to(root).as_posix() for d in ('tools/blenderctl','tools/lighting_workflow_addon') for p in (root/d).glob('*.py'))
    rows=identity['runtime_documents']
    if actual!=sorted(r['file'] for r in rows):raise ValueError('Runtime inventory changed')
    for row in rows:
        if sha(root/row['file'])!=row['expected_sha256']:raise ValueError('Runtime bytes changed: '+row['file'])
    computed=hashlib.sha256(json.dumps(sorted(rows,key=lambda r:r['file']),sort_keys=True,separators=(',',':')).encode()).hexdigest()
    if computed!=identity['implementation_sha256']:raise ValueError('Implementation identity changed')
    private=[];broken=[];links=0
    patterns=[r'[A-Z]:[\\/](?:Users|Blender AI|Blender Models)[\\/]',r'\.dsh[\\/]memory-lancedb-pro',r'ghp_[A-Za-z0-9]{20,}',r'github_pat_[A-Za-z0-9_]{20,}',r'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----',r'wm-2026-',r'runtime/audit/']
    for path in files:
        if path.suffix not in ('.py','.md','.json','.toml','.ps1','.yml','.txt'):continue
        text=path.read_text(encoding='utf-8-sig')
        if path.name!='verify_distribution.py' and any(re.search(x,text,re.I) for x in patterns):private.append(path.relative_to(root).as_posix())
        if path.suffix=='.md':
            for raw in re.findall(r'!?\[[^\]]+\]\(([^)]+)\)',text):
                target=raw.strip('<>').split('#',1)[0]
                if not target or re.match(r'^[a-z]+://',target):continue
                links+=1
                if not (path.parent/target).exists():broken.append((path.relative_to(root).as_posix(),target))
    if private or broken:raise ValueError(json.dumps({'private_patterns':private,'broken_links':broken}))
    archive='not_run'
    if extension:
        ref=identity['extension_archive']
        if sha(extension)!=ref['sha256'] or extension.stat().st_size!=ref['bytes']:raise ValueError('Extension ZIP changed')
        with zipfile.ZipFile(extension) as z:
            members={p.name:p for p in (root/'tools/lighting_workflow_addon').iterdir()
                     if p.is_file() and (p.suffix=='.py' or p.name=='blender_manifest.toml')}
            if sorted(z.namelist())!=sorted(members) or z.testzip() is not None:raise ValueError('Extension member inventory changed')
            for name,path in members.items():
                if z.read(name)!=path.read_bytes():raise ValueError('Extension member changed: '+name)
        archive='passed'
    return {'ok':True,'files':len(files),'runtime_files':len(rows),'implementation_sha256':computed,'local_links':links,'private_matches':0,'extension_archive':archive,'scope':'exact allowlist/bytes/finite patterns; no Blender/Linux runtime claim'}
def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--extension-zip',type=Path);a=p.parse_args()
    try:print(json.dumps(verify(a.root.resolve(),a.extension_zip),indent=2));return 0
    except Exception as e:print(json.dumps({'ok':False,'error':str(e)},indent=2));return 1
if __name__=='__main__':raise SystemExit(main())
