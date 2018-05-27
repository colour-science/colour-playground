# -*- coding: utf-8 -*-
"""
Widgets
=======
"""

from __future__ import division, unicode_literals

import numpy as np
from IPython.core.display import HTML
from ipywidgets.widgets import (Box, Dropdown, HBox, IntSlider, Label,
                                Textarea, VBox)

import colour

from common import NUKE_COLORMATRIX_NODE_TEMPLATE, nuke_format_matrix

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2018 - Colour Developers'
__license__ = 'New BSD License - http://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = [
    'set_style', 'RGB_colourspace_models_transformation_matrix_widget',
    'RGB_colourspace_models_chromatically_adapted_primaries_widget'
]


def set_style():

    style = """
    <style>
    .widget-container, .widget-textarea, .widget-dropdown {
        border-radius: 6px;
    }
    
    .widget-title {
        font-size: 150%;
        text-align: center;
    }
    
    .widget-label {
        font-weight: bold;
    }
    
    .widget-output-textarea {
        font-family: monospace;
    }
    </style>
    """

    return HTML(style)


def RGB_colourspace_models_transformation_matrix_widget():

    title_Label = Label('RGB Colourspace Models Transformation Matrix')
    title_Label.add_class('widget-title')

    default_layout = {'flex': '1 1 auto', 'width': 'auto'}
    input_colourspace_Dropdown = Dropdown(
        options=sorted(colour.RGB_COLOURSPACES), layout=default_layout)

    output_colourspace_Dropdown = Dropdown(
        options=sorted(colour.RGB_COLOURSPACES), layout=default_layout)

    chromatic_adaptation_transforms_Dropdown = Dropdown(
        options=sorted(colour.CHROMATIC_ADAPTATION_TRANSFORMS),
        layout=default_layout)

    formatter_Dropdown = Dropdown(
        options=['str', 'repr', 'Nuke'], layout=default_layout)

    decimals_IntSlider = IntSlider(value=10, max=15, layout=default_layout)

    RGB_to_RGB_matrix_Textarea = Textarea(rows=3, layout=default_layout)
    RGB_to_RGB_matrix_Textarea.add_class('widget-output-textarea')

    def set_RGB_to_RGB_matrix_Textarea():
        M = colour.RGB_to_RGB_matrix(
            colour.RGB_COLOURSPACES[input_colourspace_Dropdown.value],
            colour.RGB_COLOURSPACES[output_colourspace_Dropdown.value],
            chromatic_adaptation_transforms_Dropdown.value)

        with colour.utilities.numpy_print_options(
                formatter={
                    'float':
                    ('{{:0.{0}f}}'.format(decimals_IntSlider.value)).format
                },
                threshold=np.nan):
            if formatter_Dropdown.value == 'str':
                M = str(M)
            elif formatter_Dropdown.value == 'repr':
                M = repr(M)
            else:
                M = NUKE_COLORMATRIX_NODE_TEMPLATE.format(
                    nuke_format_matrix(M, decimals_IntSlider.value),
                    '{0}_to_{1}'.format(
                        input_colourspace_Dropdown.value.replace(' ', '_'),
                        output_colourspace_Dropdown.value.replace(' ', '_')))

            RGB_to_RGB_matrix_Textarea.rows = len(M.split('\n'))
            RGB_to_RGB_matrix_Textarea.value = M

    def on_input_change(change):
        if change['type'] == 'change' and change['name'] == 'value':
            set_RGB_to_RGB_matrix_Textarea()

    input_colourspace_Dropdown.observe(on_input_change)
    output_colourspace_Dropdown.observe(on_input_change)
    chromatic_adaptation_transforms_Dropdown.observe(on_input_change)
    formatter_Dropdown.observe(on_input_change)
    decimals_IntSlider.observe(on_input_change)

    set_RGB_to_RGB_matrix_Textarea()

    widget = Box([
        VBox(
            [
                title_Label,
                Textarea(
                    'This widget computes the colour transformation '
                    'matrix from the Input RGB Colourspace to the '
                    'Output RGB Colourspace using the given '
                    'Chromatic Adaptation Transform.',
                    rows=2,
                    layout=default_layout),
                Label('Input RGB Colourspace'),
                input_colourspace_Dropdown,
                Label('Output RGB Colourspace'),
                output_colourspace_Dropdown,
                Label('Chromatic Adaptation Transform'),
                chromatic_adaptation_transforms_Dropdown,
                Label('Formatter'),
                formatter_Dropdown,
                HBox([Label('Decimals:'), decimals_IntSlider]),
                Label('RGB Transformation Matrix'),
                RGB_to_RGB_matrix_Textarea,
            ],
            layout={
                'border': 'solid 2px',
                'width': '55%'
            })
    ])

    return widget


def RGB_colourspace_models_chromatically_adapted_primaries_widget():

    title_Label = Label(
        'RGB Colourspace Models Chromatically Adapted Derivation')
    title_Label.add_class('widget-title')

    default_layout = {'flex': '1 1 auto', 'width': 'auto'}
    input_colourspace_Dropdown = Dropdown(
        options=sorted(colour.RGB_COLOURSPACES), layout=default_layout)

    illuminant_Dropdown = Dropdown(
        options=sorted(
            colour.ILLUMINANTS['CIE 1931 2 Degree Standard Observer']),
        layout=default_layout)

    chromatic_adaptation_transforms_Dropdown = Dropdown(
        options=sorted(colour.CHROMATIC_ADAPTATION_TRANSFORMS),
        layout=default_layout)

    formatter_Dropdown = Dropdown(
        options=['str', 'repr'], layout=default_layout)

    decimals_IntSlider = IntSlider(value=10, max=15, layout=default_layout)

    primaries_Textarea = Textarea(rows=3, layout=default_layout)
    primaries_Textarea.add_class('widget-output-textarea')

    def set_primaries_Textarea():
        input_colourspace = colour.RGB_COLOURSPACES[
            input_colourspace_Dropdown.value]

        P = colour.chromatically_adapted_primaries(
            input_colourspace.primaries, input_colourspace.whitepoint,
            colour.ILLUMINANTS['CIE 1931 2 Degree Standard Observer'][
                illuminant_Dropdown.value],
            chromatic_adaptation_transforms_Dropdown.value)

        with colour.utilities.numpy_print_options(
                formatter={
                    'float':
                    ('{{:0.{0}f}}'.format(decimals_IntSlider.value)).format
                },
                threshold=np.nan):
            if formatter_Dropdown.value == 'str':
                P = str(P)
            elif formatter_Dropdown.value == 'repr':
                P = repr(P)

            primaries_Textarea.rows = len(P.split('\n'))
            primaries_Textarea.value = P

    def on_input_change(change):
        if change['type'] == 'change' and change['name'] == 'value':
            set_primaries_Textarea()

    input_colourspace_Dropdown.observe(on_input_change)
    illuminant_Dropdown.observe(on_input_change)
    chromatic_adaptation_transforms_Dropdown.observe(on_input_change)
    formatter_Dropdown.observe(on_input_change)
    decimals_IntSlider.observe(on_input_change)

    set_primaries_Textarea()

    widget = Box([
        VBox(
            [
                title_Label,
                Textarea(
                    'This widget computes the Chromatically Adapted Primaries '
                    'of the given RGB Colourspace Model to the given '
                    'Illuminant using the '
                    'given Chromatic Adaptation Transform.',
                    rows=3,
                    layout=default_layout),
                Label('Input RGB Colourspace'),
                input_colourspace_Dropdown,
                Label('Illuminant'),
                illuminant_Dropdown,
                Label('Chromatic Adaptation Transform'),
                chromatic_adaptation_transforms_Dropdown,
                Label('Formatter'),
                formatter_Dropdown,
                HBox([Label('Decimals:'), decimals_IntSlider]),
                Label('RGB Transformation Matrix'),
                primaries_Textarea,
            ],
            layout={
                'border': 'solid 2px',
                'width': '55%'
            })
    ])

    return widget
