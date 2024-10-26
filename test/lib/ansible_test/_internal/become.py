"""Become abstraction for interacting with test hosts."""
from __future__ import annotations

import abc
import shlex
import typing as t

from .util import (
    get_subclasses,
)


class Become(metaclass=abc.ABCMeta):
    """Base class for become implementations."""
    @property
    @abc.abstractmethod
    def method(self):  # type: () -> str
        """The name of the Ansible become plugin that is equivalent to this."""

    @abc.abstractmethod
    def prepare_command(self, command):  # type: (t.List[str]) -> t.List[str]
        """Return the given command, if any, with privilege escalation."""


class Doas(Become):
    """Become using 'doas'."""
    @property
    def method(self):  # type: () -> str
        """The name of the Ansible become plugin that is equivalent to this."""
        raise NotImplementedError('Ansible has no built-in doas become plugin.')

    def prepare_command(self, command):  # type: (t.List[str]) -> t.List[str]
        """Return the given command, if any, with privilege escalation."""
        become = ['doas', '-n']

        if command:
            become.extend(['sh', '-c', shlex.join(command)])
        else:
            become.extend(['-s'])

        return become


class Su(Become):
    """Become using 'su'."""
    @property
    def method(self):  # type: () -> str
        """The name of the Ansible become plugin that is equivalent to this."""
        return 'su'

    def prepare_command(self, command):  # type: (t.List[str]) -> t.List[str]
        """Return the given command, if any, with privilege escalation."""
        become = ['su', '-l', 'root']

        if command:
            become.extend(['-c', shlex.join(command)])

        return become


class Sudo(Become):
    """Become using 'sudo'."""
    @property
    def method(self):  # type: () -> str
        """The name of the Ansible become plugin that is equivalent to this."""
        return 'sudo'

    def prepare_command(self, command):  # type: (t.List[str]) -> t.List[str]
        """Return the given command, if any, with privilege escalation."""
        become = ['sudo', '-in']

        if command:
            become.extend(['sh', '-c', shlex.join(command)])

        return become


SUPPORTED_BECOME_METHODS = {cls.__name__.lower(): cls for cls in get_subclasses(Become)}
