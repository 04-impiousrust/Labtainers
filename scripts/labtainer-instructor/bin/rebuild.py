#!/usr/bin/env python
'''
This software was created by United States Government employees at 
The Center for the Information Systems Studies and Research (CISR) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
'''

# Filename: redo.py
# Description:
# For lab development testing workflow.  This will stop containers of a lab, create or update lab images
# and start the containers.
#

import sys
import os
import argparse
instructor_cwd = os.getcwd()
student_cwd = instructor_cwd.replace('labtainer-instructor', 'labtainer-student')
# Append Student CWD to sys.path
sys.path.append(student_cwd+"/bin")
import labutils
import logging
import LabtainerLogging
import validate

# Usage: redo.py <labname> [-f]
# Arguments:
#    <labname> - the lab to stop, delete and start
#    [-f] will force a rebuild
#    [-q] will load the lab using a predetermined email.
def main():
    parser = argparse.ArgumentParser(description='Build the images of a lab')
    parser.add_argument('labname', help='The lab to build')
    parser.add_argument('-f', '--force', action='store_true', help='force build')
    parser.add_argument('-p', '--prompt', action='store_true', help='prompt for email, otherwise use stored')
    parser.add_argument('-c', '--container', action='store', help='force rebuild just this container')
    parser.add_argument('-i', '--ignore_validate', action='store', help='ignore validation errors', default=False)
    parser.add_argument('-t', '--test_registry', action='store_true', default=False, help='build from images in the test registry')
    parser.add_argument('-L', '--no_pull', action='store_true', default=False, help='Local building, do not pull from internet')

    args = parser.parse_args()
    if args.test_registry:
        if os.getenv('TEST_REGISTRY') is None:
            #print('use putenv to set it')
            os.putenv("TEST_REGISTRY", "TRUE")
            ''' why does putenv not set the value? '''
            os.environ['TEST_REGISTRY'] = 'TRUE'
        else:
            #print('exists, set it true')
            os.environ['TEST_REGISTRY'] = 'TRUE'
        print('set TEST REG to %s' % os.getenv('TEST_REGISTRY'))
    quiet_start = True
    if args.prompt == True:
        quiet_start = False
    if args.force is not None:
        force_build = args.force
    labutils.logger = LabtainerLogging.LabtainerLogging("labtainer.log", args.labname, "../../config/labtainer.config")
    labutils.logger.INFO("Begin logging Rebuild.py for %s lab" % args.labname)
    lab_path = os.path.join(os.path.abspath('../../labs'), args.labname)
    validatetestsets = False
    validatetestsets_path = ""
    ok = validate.DoValidate(lab_path, args.labname, validatetestsets, validatetestsets_path, labutils.logger)
    if not ok and not args.ignore_validate:
        print('validation failed, exiting')
        exit(1)
    labutils.RebuildLab(lab_path, "instructor", force_build=force_build, quiet_start=quiet_start, just_container=args.container, no_pull=args.no_pull)

    return 0

if __name__ == '__main__':
    sys.exit(main())

