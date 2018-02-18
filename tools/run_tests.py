#! /usr/bin/env python3 -b

import click, os, subprocess, textwrap

test_dir = './tests'
out_dir = './run_tests/out'
check_dir = './run_tests/check'

quick_scenes = [
    'cornell_box.obj',
    'basic_pl.obj',
    'basic_al.obj',
    'simple_pl.obj',
    'simple_al.obj',
    'subdiv_al.obj',
    'plastics_al.obj',
    'plastics_el.obj',
    'metals_al.obj',
    'metals_el.obj',
    'tesselation_pl.obj',
    'lines_al.gltf',
    'points_al.gltf',
    'instancel_pl.gltf',
]

quick_view_scenes = ( [ s.rpartition('.')[0]+'.obj'  for s in quick_scenes ] +
                      [ s.rpartition('.')[0]+'.gltf' for s in quick_scenes ] )

# def run_cmds(cmds):
#     num = len(cmds)
#     for idx, cmd in enumerate(cmds, 1):
#         print(f'[CMD {idx}/{num}] {cmd}')
#         ok = not subprocess.run(cmd, shell=True).returncode
#         if not ok:
#             print(f'[ERR {idx}/{num}] {cmd}')
#         else:
#             print(f'[OK  {idx}/{num}]', end='\r')

def run_cmds(cmds):
    def shorten(cmd):
        if not cmd: return ''
        scmd = textwrap.wrap(cmd,width=50)[0] + ' ...'
        scmd += ' ' * (54 - len(scmd))
        return scmd
    with click.progressbar(cmds, width=10, show_pos=True, show_percent=False, show_eta=False, item_show_func=shorten) as bar:
        for cmd in bar:
            ok = not subprocess.run(cmd, shell=True).returncode
            if not ok: print(f'[ERR] {cmd}')

@click.group()
def run():
    pass

def run_image_tests(name, scenes, cmd, testgen=True, copycheck=False):
    odir = f'{out_dir}/{name}'
    cdir = f'{check_dir}/{name}'
    cmds = []
    cmds += [f'./tools/build.py release']
    cmds += [f'rm -rf {odir} && mkdir -p {odir}']
    if copycheck:
        cmds += [f'rm -rf {cdir} && mkdir -p {cdir}']
    if testgen:
        cmds += [f'./bin/ytestgen -q -c']
    for sname in scenes:
        sdir = test_dir + '/' + sname.partition('.')[0]
        cmds += [ f'{cmd} -o {odir}/{sname}.png {sdir}/{sname}' ]
        if copycheck:
            cmds += [ f'cp {odir}/{sname}.png {cdir}/{sname}.png' ]
        else:
            cmds += [ f'diff {odir}/{sname}.png {cdir}/{sname}.png' ]
    run_cmds(cmds)

@run.command()
@click.option('--copycheck', '-c', is_flag=True, default=False)
@click.option('--testgen', '-t', is_flag=True, default=False)
def etrace(copycheck=False,testgen=False):
    run_image_tests('etrace', quick_scenes, './bin/ytrace -q --shader eyelight -s 1 -r 360', testgen, copycheck)

@run.command()
@click.option('--copycheck', '-c', is_flag=True, default=False)
@click.option('--testgen', '-t', is_flag=True, default=False)
def qtrace(copycheck=False,testgen=False):
    run_image_tests('qtrace', quick_scenes, './bin/ytrace -q -s 16 -r 360', testgen, copycheck)

@run.command()
@click.option('--copycheck', '-c', is_flag=True, default=False)
@click.option('--testgen', '-t', is_flag=True, default=False)
def qview(copycheck=False,testgen=False):
    run_image_tests('qview', quick_view_scenes, './bin/yview -q --screenshot-and-exit --no-widgets -r 180', testgen, copycheck)

if __name__ == '__main__':
    run()
