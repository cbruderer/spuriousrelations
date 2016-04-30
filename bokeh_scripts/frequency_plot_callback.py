# see https://github.com/bokeh/bokeh-demos/blob/master/weather/main.py
from __future__ import print_function, division, absolute_import, unicode_literals
import numpy as np
import matplotlib.pyplot as plt

from bokeh.palettes import Spectral3
from bokeh.io import curdoc, vform
from bokeh.models import ColumnDataSource, DataRange1d, Range1d, VBoxForm, HBox, VBox, CustomJS, Slider
from bokeh.models.widgets import Select
from bokeh.plotting import Figure, output_file, show
from bokeh.embed import components
from bokeh.resources import CDN

def get_keys(path='keywords.txt'):
    keys = np.genfromtxt(path, dtype="|S20", delimiter='#', autostrip=True)
    return keys

def key2index(key):
    keys = get_keys()
    if len(list(np.where([keys == key])[0])) == 0:
        raise ValueError('Keyword %s not part of keyword list.' % key)
    elif len(list(np.where([keys == key])[0])) > 1:
        raise ValueError('Keyword %s occurs multiple times in keyword list.' % key)
    else:
        return np.where(keys == key)[0][0]

def freq_plot(freq_array, date_array, plot_name,
              init_key1='obama', init_key2='terrorism'):
    """
    create frequency plot
    :param freq_array: columns: dates, rows: keywords
    :param date_array: dates
    :param plot_name:
    """

    def get_dataset(key1, key2):
        return ColumnDataSource(data=dict(dates=date_array.tolist(),
                                          freq1=freq_array[key2index(key1), :].tolist(),
                                          freq2=freq_array[key2index(key2), :].tolist(),
                                          ))

    source = get_dataset(init_key1, init_key2)

    freq_list = freq_array.tolist()
    freq = ColumnDataSource(data=dict(freq_list=freq_list))

    callback1 = CustomJS(args=dict(source=source, freq=freq), code="""
                var data = source.get('data');
                var freq = freq.get('data');
                var freq_list = freq['freq_list'];
                var option = cb_obj.get('value');
                var index = option.split(':')[0];
                for (var i = 0; i < freq_list[0].length; i++)
                {data['freq1'][i] = freq_list[index][i]
                };
                source.trigger('change');
                """)
    callback2 = CustomJS(args=dict(source=source, freq=freq), code="""
                var data = source.get('data');
                var freq = freq.get('data');
                var freq_list = freq['freq_list'];
                var option = cb_obj.get('value');
                var index = option.split(':')[0];
                for (var i = 0; i < freq_list[0].length; i++)
                {data['freq2'][i] = freq_list[index][i]
                };
                source.trigger('change');
                """)

    # set up plot
    plot = Figure(plot_width=1000, tools="pan,reset,"
                                         "resize,save,wheel_zoom",
                  responsive=True)
    plot.min_border=0
    colormap = Spectral3

    keys = get_keys()
    for i in range(len(keys)):
        plot.line(x=date_array.tolist(), y=freq_array[i, :].tolist(),
                  line_color=colormap[1], line_alpha=0.5,
                  line_width=1)

    plot.line(x='dates', y='freq1',
              line_width=4,
              line_alpha=1, source=source,
              line_color=colormap[0],
              legend='keyword 1')
    plot.line(x='dates', y='freq2',
              line_width=4,
              line_alpha=1, source=source,
              line_color=colormap[2],
              legend='keyword 2')
    plot.xaxis.axis_label = 'Date'
    plot.yaxis.axis_label = 'Variation relative to mean'
    plot.legend.location = 'top_right'

    # set up widgets
    options = [str(x) + ': ' + get_keys()[x] for x in range(len(get_keys()))]
    first_key1 = str(key2index(init_key1)) + ': ' + init_key1
    first_key2 = str(key2index(init_key2)) + ': ' + init_key2

    key1_select = Select(value=first_key1, title='keyword 1',
                         options=options,
                         callback=callback1)
    key2_select = Select(value=first_key2, title='keyword 2',
                         options=options,
                         callback=callback2)

    inputs = HBox(key1_select, key2_select, width=400)

    layout = VBox(inputs, plot)
    # layout = vform(inputs, plot)

    # for website
    script, html = components(layout)
    print (html)

    # curdoc().add_root(HBox(inputs, plot))

    # save output file
    output_file(plot_name + '.html', title=plot_name)

    # save js file for website
    js_file = open(plot_name + '.js', 'w')
    js_file.write(script)
    js_file.close()

    show(layout)

# testing
frequencies = np.random.rand(100, 100)
dates = np.arange(0, 100, 1)
freq_plot(frequencies, dates, 'frequency_plot')
