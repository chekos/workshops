'''
creates functions to use along with blog post notebook
'''

import pandas as pd
import altair as alt
from ipywidgets import interact

df = pd.read_csv('immigrants blog post (clean).csv', index_col = 0, parse_dates = ['year'], )

df['perwt'] = df['perwt'].astype(int)
df = df[df['year'] > '1980-01-01']


top_countries = df.groupby('bpld')['perwt'].sum().to_frame().reset_index().copy()
top_countries = top_countries[top_countries['perwt'] >= 5000]
top_countries = [country for country in top_countries['bpld']]
top_countries.pop(0) # this gets rid of 'Abroad, n.s.'

scale_top5 = alt.Scale(domain=['China', 'Mexico', 'Philippines', 'Vietnam', 'India'],
                 range=['#E98426', '#905A78', '#D2AA1D', '#0D828A', '#B44B27'])

scale_educ = alt.Scale(domain = ['Ba Or More', 'Some College', 'Hs', 'Less Than Hs', ],
                      range = ['#004A80', '#649EA5', '#73A57A', '#D2AA1D', ], type = 'ordinal', )

def bar_chart(country):
    '''
    creates an altair interactive barchart. Expects "country"
    '''
    
    data = df[df['year'] > '1990-01-01'].copy()
    data['year'] = data['year'].dt.year

    return (
        alt.Chart(data[data['bpld'] == country])
        .mark_bar()
        .encode(
            x=alt.X('year:O', axis=alt.Axis(title='Year',),),
            y=alt.Y('perwt:Q', axis=alt.Axis(title='Number of People',),),
            color=alt.Color(
                'agg educd',
                legend=alt.Legend(title='Educational Attainment'),
                scale=scale_educ,
            ),
        )
        .properties(title=f'{country}'.capitalize(), width=500, height=300,)
    )
    
def line_chart():
    '''
    creates altair interactive line chart for top 5 countries
    '''

    top_5 = df[((df['bpld'] == 'China') | (df['bpld'] == 'Mexico') | (df['bpld'] == 'Philippines') | (df['bpld'] == 'Vietnam') | (df['bpld'] == 'India'))].copy()
    top_5.drop(columns = ['agg educd'], inplace = True)
    top_5 = top_5.groupby(['year', 'bpld'])['perwt'].sum().to_frame().reset_index().copy()

    brush = alt.selection(type = 'interval', encodings = ['x'],)

    upper_chart = alt.Chart(top_5).mark_line().encode(
        x = alt.X('year:T', scale = {'domain': brush.ref()}, axis = alt.Axis(title = 'Year', format = '%Y') ,),
        y = alt.Y('perwt:Q', axis = alt.Axis(title = 'Number of People',), ),
        color = alt.Color('bpld', legend = alt.Legend(title = 'Birthplace'), scale = scale_top5),
    ).properties(
        title = 'Top 5',
        width = 600,
        height = 300,
    )

    # This might not be best practices
    # Essentially I'm creating really big circles around each point and making them 100% transparent
    # whenever the mouse is on top of a circle the tooltip will display the value. Hence the big circles.
    upper_chart_points = upper_chart.mark_point(size = 500).encode(tooltip = alt.Tooltip('perwt:Q', format = ',',), opacity = alt.value(0))

    # Layers
    upper_chart_layered = upper_chart + upper_chart_points

    # Creates smaller chart to use as slider
    lower_chart = upper_chart.encode(
        x = alt.X('year:T', axis = alt.Axis(title = 'Slider', format = '%Y') ,),
        y = alt.Y('perwt:Q', axis = alt.Axis(title = '', labels = False, ticks = False,), ),
    ).properties(
        title = '',
        selection = brush,
        height = 30,
    )

    return alt.vconcat(upper_chart_layered, lower_chart)

def education_chart():
    '''
    creates altair line chart for educational attainment levels across time for recently arrived immigrants.
    '''
    
    education = df.groupby(['year', 'agg educd'])['perwt'].sum().to_frame().reset_index()

    
    education_chart = alt.Chart(education).mark_line().encode(
        x = alt.X('year:T', axis = alt.Axis(title = 'Year', format = '%Y',),),
        y = alt.Y('perwt:Q', axis = alt.Axis(title = 'Number of People',),),
        color = alt.Color('agg educd', legend = alt.Legend(title = 'Educational Attainment') ),
    ).properties(
        width = 600,
        height = 400,
        title = 'Educational Attainment Levels Across Time (recently arrived immigrants)',
    )
    
    educ_points = education_chart.mark_point(size = 500).encode(tooltip = alt.Tooltip('perwt:Q', format = ',g',), opacity = alt.value(0))
    
    return education_chart + educ_points
