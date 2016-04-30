import numpy as np

def corr_plot(corr_array, plot_name):

    from bokeh.plotting import figure, show, output_file
    from bokeh.models import HoverTool, ColumnDataSource
    from bokeh.palettes import Spectral10
    from bokeh.embed import components

    import read_keywords

    nodes = np.arange(0, np.shape(corr_array)[0], 1)
    names = list(read_keywords.get_keys())

    # colormap = ["#444444", "#a6cee3", "#1f78b4", "#b2df8a", "#33a02c", "#fb9a99",
    #             "#e31a1c", "#fdbf6f", "#ff7f00", "#cab2d6"]
    colormap = Spectral10
    print (colormap)

    xname = []
    yname = []
    color = []
    corr_value = []

    for i in range(len(nodes)):
        for j in range(len(nodes)):
            xname.append(names[i])
            yname.append(names[j])

            corr_value.append(corr_array[i, j])
            color.append(colormap[int(corr_array[i, j] * 10)])

    source = ColumnDataSource(data=dict(
                                        xname=xname,
                                        yname=yname,
                                        colors=color,
                                        corr=corr_value,
                                        ))
    p = figure(title="Correlations",
               x_axis_location="above", tools="resize,hover,pan,box_zoom,wheel_zoom,reset",
               x_range=list(reversed(names)), y_range=names)

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
    output_file(plot_name + '.html', title=plot_name)

    # for website
    script, div = components(p)

    # save js file for website
    js_file = open(plot_name + '.js', 'w')
    js_file.write(script)
    js_file.close()

    print div

    show(p)

test_array = np.random.rand(100, 100)
corr_plot(test_array, 'correlations_plot')
