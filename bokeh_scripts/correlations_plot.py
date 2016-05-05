import numpy as np

def corr_plot(corr_array, title, plot_name):

    from bokeh.plotting import figure, show, output_file
    from bokeh.models import HoverTool, ColumnDataSource
    from bokeh.palettes import Spectral10
    from bokeh.embed import components

    import read_keywords

    nodes = np.arange(0, np.shape(corr_array)[0], 1)
    names = list(read_keywords.get_keys())

    colormap = Spectral10

    xname = []
    yname = []
    color = []
    corr_value = []

    value_bins = np.linspace(-1, 1, 10)

    def get_color(value):
        ind = np.digitize([value], value_bins)
        return ind[0]-1

    for i in range(len(nodes)):
        for j in range(len(nodes)):
            xname.append(names[i])
            yname.append(names[j])
            corr_value.append(corr_array[i, j])
            color.append(colormap[get_color(corr_array[i, j])])

    source = ColumnDataSource(data=dict(
                                        xname=xname,
                                        yname=yname,
                                        colors=color,
                                        corr=corr_value,
                                        ))
    p = figure(title=title,
               x_axis_location="above", tools="resize,hover,pan,box_zoom,wheel_zoom,reset",
               x_range=list(reversed(names)), y_range=names, responsive=True)

    p.plot_width = 800
    p.plot_height = 800
    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_text_font_size = "5pt"
    p.axis.major_label_standoff = 0
    p.xaxis.major_label_orientation = np.pi/3

    p.rect('xname', 'yname', 0.9, 0.9, source=source,
           color='colors', line_color=None)

    p.select_one(HoverTool).tooltips = [
        ('keywords', '@yname, @xname'),
        ('value', '@corr'),
    ]

    # save output file
    output_file(plot_name + '.html', title=title)

    # for website
    script, div = components(p)

    # save js file for website
    js_file = open(plot_name + '.js', 'w')
    js_file.write(script)
    js_file.close()

    print div

    show(p)


# raw
raw_array = np.load('correlations_raw.npy')
raw_title = 'Correlations between Time Series'
raw_plot_name = 'correlations_raw'

corr_plot(raw_array, raw_title, raw_plot_name)

diff_array = np.load('correlations_diff.npy')
diff_title = 'Correlations between Differenced Time Series'
diff_plot_name = 'correlations_diff'

# corr_plot(diff_array, diff_title, diff_plot_name)
