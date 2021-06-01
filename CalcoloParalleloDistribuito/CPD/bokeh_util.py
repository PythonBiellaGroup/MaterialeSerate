import math

# SOURCE: https://github.com/anyscale/academy/blob/5046fdb4d94fcd7b9be6fa44e877283d401345c7/ray-crash-course/01-Ray-Tasks.ipynb


import bokeh.io
# For graphs
from bokeh.plotting import figure

# The next two lines prevent Bokeh from opening the graph in a new window.
bokeh.io.reset_output()
bokeh.io.output_notebook()

def two_lines_plot(title, x_label, y_label, line_one_label, line_two_label,
                   ns, durations, ray_ns, ray_durations, x_axis_type='log', y_axis_type='log'):
    tooltips = [
        ("name", "$name"),
        ("array size", "$x"),
        ("time", "$y")]
    plot = figure(x_axis_type=x_axis_type, y_axis_type=y_axis_type, title=title, tooltips=tooltips)
    plot.grid.grid_line_alpha = 0.3
    plot.xaxis.axis_label = x_label
    plot.yaxis.axis_label = y_label

    plot.line(ns, durations, color='#A6CEE3', legend_label=line_one_label, name=line_one_label)
    plot.circle(ns, durations, color='#A6CEE3', size=4)

    plot.line(ray_ns, ray_durations, color='#B2DF8A', legend_label=line_two_label, name=line_two_label)
    plot.square(ray_ns, ray_durations, color='#B2DF8A', size=4)
    plot.legend.location = "top_left"

    return plot


def means_stddevs_plot(ns, means, stddevs, title=''):
    tooltips = [
        ("name", "$name"),
        ("array size", "$x"),
        ("time", "$y")]
    plot = figure(x_axis_type="log", title=title, tooltips=tooltips, sizing_mode='stretch_both')
    plot.grid.grid_line_alpha = 0.5
    plot.xaxis.axis_label = 'N'
    plot.yaxis.axis_label = ''

    # Draw a line for correct Pi value.
    plot.segment(x0=ns[0] * 0.8, y0=[math.pi], x1=ns[-1] * 1.2, y1=[math.pi],
                 color="red", line_width=2, legend_label='π', name='π')

    plot.line(ns, means, color='#A6CEE3', legend_label='mean', name='mean')
    plot.circle(ns, means, color='#A6CEE3', size=10)

    # Draw std. dev. lines.
    m_ss = list(zip(means, stddevs))
    minus_stddevs = list(map(lambda m_s: m_s[0] - m_s[1], m_ss.copy()))
    plus_stddevs = list(map(lambda m_s: m_s[0] + m_s[1], m_ss.copy()))

    plot.segment(x0=ns, y0=minus_stddevs, x1=ns, y1=plus_stddevs,
                 color="black", line_width=2, legend_label='std. dev.', name='σ')

    # "Whiskers" at the end of the std. dev. lines
    # (almost-0 height rects simpler than segments)
    widths = list(map(lambda x: x / 10.0, ns.copy()))
    plot.rect(x=ns, y=minus_stddevs, width=widths, height=0.0001, fill_color="black")
    plot.rect(x=ns, y=plus_stddevs, width=widths, height=0.0001, fill_color="black")

    plot.legend.location = "bottom_right"

    return plot
