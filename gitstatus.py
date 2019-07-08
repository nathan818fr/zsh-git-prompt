#!/usr/bin/env python
from __future__ import print_function

# change this symbol to whatever you prefer
prehash = ':'

import sys
from subprocess import Popen, PIPE


# `git status --porcelain -b` can collect all information
# branch, remote_branch, untracked, staged, changed, conflicts, ahead, behind
po = Popen(['git', 'status', '--porcelain', '-b', '-uno'], stdout=PIPE, stderr=PIPE)
stdout, sterr = po.communicate()
if po.returncode != 0:
    sys.exit(0)  # Not a git repository

# collect git status information
untracked, staged, changed, conflicts = [], [], [], []
ahead, behind = 0, 0
status = [(line[0], line[1], line[2:]) for line in stdout.splitlines()]
for st in status:
    if st[0] == '#' and st[1] == '#':
        st2 = st[2].replace('No commits yet on ', '').strip()
        if len(st2.split('...')) == 1:
            branch = st2
        else:
            # current and remote branch info
            branch, rest = st2.split('...')
            if len(rest.split(' ')) == 1:
                # remote_branch = rest.split(' ')[0]
                pass
            else:
                # ahead or behind
                divergence = ' '.join(rest.split(' ')[1:])
                divergence = divergence.lstrip('[').rstrip(']')
                for div in divergence.split(', '):
                    if 'ahead' in div:
                        ahead = int(div[len('ahead '):].strip())
                    elif 'behind' in div:
                        behind = int(div[len('behind '):].strip())
    elif st[0] == '?' and st[1] == '?':
        untracked.append(st)
    else:
        if st[1] == 'M':
            changed.append(st)
        if st[0] == 'U':
            conflicts.append(st)
        elif st[0] != ' ':
            staged.append(st)

out = ' '.join([
    branch,
    str(ahead),
    str(behind),
    str(len(staged)),
    str(len(conflicts)),
    str(len(changed)),
    str(len(untracked)),
])
print(out, end='')

