#! /usr/bin/env python
# encoding: utf-8

import os
from waflib.TaskGen import feature, after_method

APPNAME = 'kodo-simulations-python'
VERSION = '0.0.0'

import waflib.extras.wurf_options


def options(opt):

    opt.load('wurf_common_tools')
    opt.load('python')


def resolve(ctx):

    import waflib.extras.wurf_dependency_resolve as resolve

    ctx.load('wurf_common_tools')

    ctx.add_dependency(resolve.ResolveVersion(
        name='waf-tools',
        git_repository='github.com/steinwurf/waf-tools.git',
        major=3))

    ctx.add_dependency(resolve.ResolveVersion(
        name='kodo-python',
        git_repository='github.com/steinwurf/kodo-python.git',
        major=10))


def configure(conf):

    conf.load("wurf_common_tools")


def build(bld):

    bld.load("wurf_common_tools")

    # Define a dummy task to force the compilation of the kodo-python library
    bld(features='cxx test',
        use=['kodo-python'])


@feature('test')
@after_method('apply_link')
def test_simulations(self):
    # Only execute the tests within the current project
    if self.path.is_child_of(self.bld.srcnode):
        if self.bld.has_tool_option('run_tests'):
            self.bld.add_post_fun(exec_test_simulations)


def exec_test_simulations(bld):
    python = bld.env['PYTHON'][0]
    env = dict(os.environ)
    kodo_ext = bld.get_tgen_by_name('kodo-python').link_task.outputs[0]
    env['PYTHONPATH'] = kodo_ext.parent.abspath()

    # First, run the unit tests in the 'test' folder (the unittest module
    # automatically discovers all files matching the 'test*.py' pattern)
    if os.path.exists('test'):
        cwd = 'test'
        bld.cmd_and_log('"{0}" -m unittest discover\n'.format(python),
                        cwd=cwd, env=env)

    # Then run the examples in the 'examples' folder
    if os.path.exists('examples'):
        cwd = 'examples'
        for f in sorted(os.listdir('examples')):
            if f.endswith('.py'):
                bld.cmd_and_log(
                    '"{0}" {1}\n'.format(python, f), cwd=cwd, env=env)
