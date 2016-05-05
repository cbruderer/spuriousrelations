# see https://github.com/bokeh/bokeh-demos/blob/master/weather/main.py
from __future__ import print_function, division, absolute_import, unicode_literals
import numpy as np
import matplotlib.pyplot as plt
import datetime

from bokeh.palettes import Spectral9
from bokeh.io import curdoc, vform
from bokeh.models import ColumnDataSource, DataRange1d, Range1d, VBoxForm, HBox, VBox, CustomJS, Slider
from bokeh.models.widgets import Select
from bokeh.plotting import Figure, output_file, show
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.models import HoverTool


def get_keys(path='../docs/keywords.txt'):
    keys = np.genfromtxt(path, dtype="|S20", delimiter='#', autostrip=True)
    return keys

def get_events(path='../docs/world_events_2014.txt'):
    from StringIO import StringIO
    data = np.loadtxt(path, dtype=str, delimiter=',')
    day = np.array(data[:, 0], dtype=int)
    month = np.array(data[:, 1], dtype=int)
    year = np.array(data[:, 2], dtype=int)
    return month, day, year, data[:, 3]

def key2index(key):
    keys = get_keys()
    if len(list(np.where([keys == key])[0])) == 0:
        raise ValueError('Keyword %s not part of keyword list.' % key)
    elif len(list(np.where([keys == key])[0])) > 1:
        raise ValueError('Keyword %s occurs multiple times in keyword list.' % key)
    else:
        return np.where(keys == key)[0][0]

def date2index(day, month, year):
    m, d, y, event = get_events()
    return np.where((day == d) & (month == m) & (year == y))[0][0]

def freq_plot(freq_array, date_array, plot_name,
              init_key1='tea', init_key2='coffee'):
    """
    create frequency plot
    :param freq_array: columns: dates, rows: keywords
    :param date_array: dates
    :param plot_name:
    """

    def get_dataset(key1, key2):
        return ColumnDataSource(data=dict(dates=date_array,
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
                  responsive=True, x_axis_type='datetime')
    plot.min_border = 0
    colormap = Spectral9

    keys = get_keys()
    for i in range(len(keys)):
        plot.line(x=date_array, y=freq_array[i, :].tolist(),
                  line_color=colormap[4], line_alpha=0.5,
                  line_width=1)

    plot.line(x='dates', y='freq1',
              line_width=4,
              line_alpha=1, source=source,
              line_color=colormap[0],
              legend='keyword 1',
             )
    plot.line(x='dates', y='freq2',
              line_width=4,
              line_alpha=1, source=source,
              line_color=colormap[1],
              legend='keyword 2',
              )
    plot.xaxis.axis_label = 'Date [Month/Day/Year]'
    plot.yaxis.axis_label = 'Variation relative to mean'
    plot.legend.location = 'top_right'

    # show events
    m, d, y, e = get_events()
    all_dates = [datetime.datetime(y[i], m[i], d[i]) for i in range(y.shape[0])]

    event_source = ColumnDataSource(data=dict(date_x=all_dates,
                                              date_y=[10 for x in all_dates],
                                              event=e,
                                              date=[x.strftime('%m-%d-%Y') for x in all_dates]))
    event_points = plot.circle(x='date_x', y='date_y', size=20,
                               color=colormap[8], source=event_source,
                               alpha=.5)

    hover = HoverTool(renderers=[event_points],
                      tooltips=[("date", "@date"), ("event", "@event")],
                      )
    plot.add_tools(hover)

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

import pickle
f = open('../data/datetime.pkl', 'rb')

dates = pickle.load(f)
frequencies = np.load('../data/freq_variations.npy')

freq_plot(frequencies, dates, 'frequency_plot')
