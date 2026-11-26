# SPDX-License-Identifier: GPL-3.0-or-later
"""Build exact allowlisted archives; never include a working runtime or user files."""
import argparse,hashlib,json,shutil,zipfile
from pathlib import Path
from verify_distribution import export_files,verify
def archive(path,entries):
    with zipfile.ZipFile(path,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as out:
        for name,source in sorted(entries):
            info=zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
            out.writestr(info,source.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--extension-zip',type=Path,required=True);a=p.parse_args();root=a.root.resolve()
    checks=verify(root,a.extension_zip);dest=root/'dist';dest.mkdir(exist_ok=True)
    identity=json.loads((root/'docs/runtime-identity.json').read_text());version=identity['plugin_version'];files=export_files(root)
    extension=dest/('lighting_workflow-'+version+'.zip')
    if extension.exists():raise ValueError('Existing release files are never silently replaced')
    shutil.copyfile(a.extension_zip,extension)
    source=dest/('lighting-workflow-source-'+version+'.zip');archive(source,[('blender-lighting-workflow/'+p.relative_to(root).as_posix(),p) for p in files])
    skill_version=identity['skill_version']
    skill=dest/('blender-lighting-skill-'+skill_version+'.zip');archive(skill,[(p.relative_to(root).as_posix(),p) for p in files if p.is_relative_to(root/'skills')]+[('install_skills.py',root/'scripts/install_skills.py'),('LICENSE',root/'LICENSE')])
    license_asset=dest/'LICENSE'
    with license_asset.open('xb') as output:output.write((root/'LICENSE').read_bytes())
    rows=[{'file':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in (extension,source,skill,license_asset)]
    (dest/'SHA256SUMS.txt').write_text(''.join(r['sha256']+'  '+r['file']+'\n' for r in rows),encoding='utf-8')
    (dest/'release-manifest.json').write_text(json.dumps({'tag':'v'+version,'plugin_version':version,'cli_version':identity['cli_version'],'production_cli':identity['production_cli'],'skill_version':skill_version,'implementation_sha256':identity['implementation_sha256'],'files':rows},indent=2),encoding='utf-8')
    print(json.dumps({'ok':True,'verification':checks,'files':rows},indent=2))
if __name__=='__main__':main()
