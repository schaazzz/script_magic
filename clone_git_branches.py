#--------------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2014 Shahzeb Ihsan
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

#--------------------------------------------------------------------------
## @file    clone_git_branches.py
#  @brief   Clone all branches in a Github repository with each branch in
#           its own folder.
#
#  @author  Shahzeb Ihsan [shahzeb.ihsan@gmail.com]
#  @version 0.1

#--------------------------------------------------------------------------
# Module Imports
import subprocess, os, argparse, sys
from helpers import *

#--------------------------------------------------------------------------
# Module Global Attributes
# --- N/A

#--------------------------------------------------------------------------
# Module Global Variables
# --- N/A

#--------------------------------------------------------------------------
# Module Local Attributes
# --- N/A

#--------------------------------------------------------------------------
# Module Internal Variables
# --- N/A

branches = []

if len(sys.argv) == 1:
    # If the options were not specified on the command line, get user input
    username = get_validated_input('Github username: ' )[1]
    repository = get_validated_input('Repository name: ')[1]
    path = get_validated_input('Output path: ')[1]
else:
    # Create the parser for the command line arguments
    parser = argparse.ArgumentParser(
                                prog = 'clone_git_branches',
                                formatter_class = argparse.RawDescriptionHelpFormatter,
                                usage = 'python clone_git_branches.py -u <GitHub username> -r <repository name> -p <path to clone into>',
                                description = 'Clone all branches in a Github branch with each branch in its own folder',
                                epilog = '---\n',
                                add_help = True)

    # Add the username '-u' argument
    parser.add_argument(
                    '-u',
                    action = 'store',
                    help = 'Github username')

    # Add the repository name '-r' argument
    parser.add_argument(
                    '-r',
                    action = 'store',
                    help = 'repository name')

    # Add the path '-p' argument
    parser.add_argument(
                    '-p',
                    action = 'store',
                    help = 'path to clone into')

    # Parse command line arguments
    parsed_args = parser.parse_args(sys.argv[1:])

    # Read parsed arguments
    if parsed_args.u and parsed_args.r and parsed_args.p:
        username = parsed_args.u
        repository = parsed_args.r
        path = parsed_args.p
    else:
        print 'Not enough command line arguments'
        parser.print_help()
        sys.exit(-1)

# Create repository's SSH and HTTP URLs
url_https = 'https://github.com/schaazzz/' + repository + '.git'
url_ssh = 'git@github.com:' + username + '/' + repository + '.git'

print '\r\n---'
print 'HTTPS URL: ' + url_https
print 'SSH URL: ' + url_ssh

# Retrieve all branches in the repository...
process = subprocess.Popen(
                        'git ls-remote ' + url_https,
                        shell = True,
                        stdout = subprocess.PIPE)

out, err = process.communicate()
out = out.replace('\t', ' ').replace('\n', ' ').split(' ')

for str in out:
    if 'refs/heads' in str:
        branches.append(str.replace('refs/heads/', ''))

# Create a directory using the repository's name
path = os.path.join(path, repository)
os.mkdir(path)

# Cycle through all branches...
for branch in branches:
    # ...and clone each branch, using the HTTPS URL, into its each folder
    # ...the HTTPS URL is used because it doesn't require a pass phrase entry
    command = 'git clone -b ' + branch + ' --single-branch ' + url_https + ' ' + os.path.join(path, branch)
    print '\r\n---'
    print command
    subprocess.Popen(command, shell = True).wait()

    # ...and now we finally change the remote URL to the SSH URL
    command = 'git --git-dir ' + os.path.join(path, branch, '.git') + ' remote set-url origin ' + url_ssh
    print command
    subprocess.Popen(command, shell = True).wait()
