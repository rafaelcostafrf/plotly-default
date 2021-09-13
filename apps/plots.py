import plotly.express as px

colors = {
    'background': '#ffffff',
    'text': '#000000'
}

def PlotHist(x, color, colors_values, labels_dict, range_x, nbins):
    fig = px.histogram(
                        x=x, 
                        color=color, 
                        color_discrete_sequence=colors_values,
                        labels=labels_dict,
                        range_x=range_x,
                        nbins=nbins)
    fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
    )
    fig.update_yaxes(
        showline=True, 
        linewidth=1, 
        linecolor='#f3f3f3', 
        gridcolor='#f3f3f3')
    fig.update_xaxes(
        showline=True, 
        linewidth=1, 
        linecolor='#f3f3f3', 
        gridcolor='#f3f3f3',)
    return fig

def PlotBar(df, y, colors_values, range_x):
    fig = px.bar(
        df,
        y=y,
        color_discrete_sequence=colors_values,
        range_x=range_x)

    fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
    )
    fig.update_yaxes(
        showline=True, 
        linewidth=1, 
        linecolor='#f3f3f3', 
        gridcolor='#f3f3f3')
    fig.update_xaxes(
        showline=True, 
        linewidth=1, 
        linecolor='#f3f3f3', 
        gridcolor='#f3f3f3',)
    return fig