# vim: tabstop=4 shiftwidth=4 softtabstop=4

#    Copyright (C) 2012 Yahoo! Inc. All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


class AnvilException(Exception):
    pass


class PermException(AnvilException):
    pass


class OptionException(AnvilException):
    pass


class DownloadException(AnvilException):
    pass


class InstallException(AnvilException):
    pass


class BadParamException(AnvilException):
    pass


class NoTraceException(AnvilException):
    pass


class NoReplacementException(AnvilException):
    pass


class StartException(AnvilException):
    pass


class PackageException(AnvilException):
    pass


class StopException(AnvilException):
    pass


class RestartException(AnvilException):
    pass


class StatusException(AnvilException):
    pass


class PasswordException(AnvilException):
    pass


class FileException(AnvilException):
    pass


class ConfigException(AnvilException):
    pass


class DependencyException(AnvilException):
    pass


class ProcessExecutionError(IOError):
    def __init__(self, stdout=None, stderr=None,
                 exit_code=None, cmd=None,
                 description=None):
        self.exit_code = exit_code
        self.stderr = stderr
        self.stdout = stdout
        self.cmd = cmd
        self.description = description
        if not self.cmd:
            self.cmd = '-'
        if not self.description:
            self.description = 'Unexpected error while running command.'
        if not isinstance(self.exit_code, (long, int)):
            self.exit_code = '-'
        if not self.stderr:
            self.stderr = ''
        if not self.stdout:
            self.stdout = ''
        message = ('%s\nCommand: %s\n'
                    'Exit code: %s\nStdout: %r\n'
                    'Stderr: %r' % (self.description, self.cmd,
                                            self.exit_code, self.stdout,
                                            self.stderr))
        IOError.__init__(self, message)


class YamlException(ConfigException):
    pass


class YamlOptionNotFoundException(YamlException):
    """Raised by YamlRefLoader if reference option not found."""
    def __init__(self, conf, opt, ref_conf, ref_opt):
        msg = "In `{0}`=>`{1}: '$({2}:{3})'` " \
              "reference option `{3}` not found." \
              .format(conf, opt, ref_conf, ref_opt)
        super(YamlOptionNotFoundException, self).__init__(msg)


class YamlConfigNotFoundException(YamlException):
    """Raised by YamlRefLoader if config source not found."""
    def __init__(self, path):
        msg = "Could not find (open) yaml source {0}.".format(path)
        super(YamlConfigNotFoundException, self).__init__(msg)


class YamlLoopException(YamlException):
    """Raised by YamlRefLoader if reference loop found."""
    def __init__(self, conf, opt, ref_stack):
        prettified_stack = "".join(
            "\n%s`%s`=>`%s`" % (" " * i, c, o)
            for i, (c, o) in enumerate(ref_stack))
        msg = "In `{0}`=>`{1}` reference loop found.\n" \
              "Reference stack is:{2}." \
              .format(conf, opt, prettified_stack)

        super(YamlLoopException, self).__init__(msg)
