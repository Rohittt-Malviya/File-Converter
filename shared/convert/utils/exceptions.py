"""Typed exceptions exposed to desktop and automation clients."""


class ConversionError(Exception):
    """A conversion could not be completed safely."""


class InvalidInputError(ConversionError):
    """An input file is missing, empty, or invalid."""


class UnsupportedConversionError(ConversionError):
    """The selected conversion requires unsupported input or tooling."""
