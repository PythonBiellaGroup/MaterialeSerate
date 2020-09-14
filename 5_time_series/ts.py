import pandas as pd

def find_timegaps(series, gap, gap_comparison='higher', divergent_only=False):
    """
    Find time gaps in the datetime series in input according to the gap size
    checked using the operator specified.
    The type of comparison along with the gap size define what gaps will be
    flagged. If the variable divergent_only is True, only the gaps that does
    not satisfy the comparison are returned. The returned column mask shows
    which timestamps satisfied the comparison. Each gap returned in the column
    delta is relative to the gap between the current timestamp and the previous
    one.

    Parameters
    ----------
    series : pandas.Series of dtype=datetime
        Series that represents a dataframe index, populated by timestamps.

    gap : string to be parsed to pandas.Timedelta:
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timedelta.html
        The time delta used to find time gaps higher, equal or lower with
        respect to this delta. 

    gap_comparison : {'higher', 'equal', 'lower'}
        The operator used in the comparison.

    divergent_only : bool
        Select if only the timestamps that does not satisfy the condition are
        returned.

    Returns
    -------
    DataFrame
        Dataframe with integer indexes and timestamps of the input series as
        rows, the comparison result and the time gap as columns.
    """
    delta = pd.Series(series).diff()  # [1:]

    if gap_comparison == 'higher':
        mask = delta > pd.Timedelta(gap)
    elif gap_comparison == 'lower':
        mask = delta < pd.Timedelta(gap)
    elif gap_comparison == 'equal':
        mask = delta == pd.Timedelta(gap)

    df = pd.DataFrame({
        'timestamp': series,
        'mask': mask,
        'delta': delta
        })

    if divergent_only:
        return df[df['mask'] == True]
    else:
        return df
    
    

def plot_interval(
        df,
        columns=[],
        interval='hour',
        figsize_width=11,
        figsize_height=5,
        hide_xlabel=True
        ):
    """
    Plot the distribution of the data grouped by the interval provided, for
    each column in the dataframe.

    Each column of the dataframe is plotted, if no columns are specified. Each
    column is plotted in an indipendent plot, representing a grouping of the
    column data according to the interval provided in input. The accepted
    intervals are the same as the attributes of pandas.DatetimeIndex. Depending
    on the provided interval, the plot shows either the seasonality or the
    trend.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe with time on rows and features on columns.

    columns : list of string
        Select the column of the dataframe df to plot.

    interval : string
        The time interval used to group the column data.

    figsize_width : int, >0
        The width of each plot.

    figsize_height : int, >0
        The height of each plot.

    hide_xlabel : bool
        Hide the label of the x-axis on each plot, show it only on the last
        plot.
    """
    if not columns:
        columns = df.columns
    else:
        missing = [col for col in columns if col not in df.columns]
        if missing:
            raise KeyError(f'None of {missing} are in the columns of the '
                           'dataframe provided')

    available_intervals = [
        'day',
        'dayofweek',
        'dayofyear',
        'daysinmonth',
        'hour',
        'month',
        'microsecond',
        'minute',
        'month',
        'nanosecond',
        'quarter',
        'second',
        'week',
        'weekday',
        'weekday_name',
        'weekofyear',
        'year'
        ]

    if interval not in available_intervals:
        raise ValueError(f'{interval} is not a supported interval')

    df = df.copy()
    df[interval] = getattr(df.index, interval).rename(interval)

    fig, axes = plt.subplots(
        len(columns),
        1,
        figsize=(figsize_width, len(columns)*figsize_height)
        )

    if type(axes) is not np.ndarray:
        axes = np.array([axes])

    for name, ax in zip(columns, axes):
        sns.boxplot(data=df, x=interval, y=name, ax=ax)
        ax.set_title(name)
        if hide_xlabel and ax != axes[-1]:
            ax.set_xlabel('')