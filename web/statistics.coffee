###########################################################
# © 2013/2014 Daniel 'grindhold' Brendle with torservers.net
#
# This file is part of torcollect
#
# torcollect is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License
# as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later
# version.
#
# torcollect is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE. See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with torcollect.
# If not, see http://www.gnu.org/licenses/.
############################################################

data = graphdata

# Returns the radius of the dots in the graph
get_dot_radius = -> 5

# Returns the width of the graph which is the width of the div assigned to it
graph_width = () -> return document.getElementById("graphspace").clientWidth - 20

# returns the stepwidth for the x-axis
x_space_between_points = () -> return graph_width() / (data.length - 1)

# returns the relative x position in pixel for a n-th point
get_x_position = (count) -> return Math.round count * x_space_between_points()

# returns the stepwidth
y_space_between_points = () -> return (graph_height() - get_dot_radius()*2) / maxim get_user_array data

# returns the relative y position in px for a value
get_y_position = (value) -> return Math.round graph_height() - value * y_space_between_points() + get_dot_radius()

# returns the graph's height
graph_height = () -> 100
get_point = (value, count) -> [get_x_position(count) , get_y_position (value) ]
get_point_string = (value, count) -> return get_point(value,count)[0]+","+get_point(value,count)[1]

#returns the greatest value in an array
maxim = (data, i=0) ->
    if i+1 == data.length
        return Math.max(-Infinity,data[i])
    else
        return Math.max(data[i],maxim data, i+1)

#returns the values of a dict as array
values = (dictionary) ->
    (v for k,v of  dictionary)

#returns the keys of a dict as array
keys = (dictionary) ->
    (k for k,v of dictionary)

# return user_array in data
get_user_array = (data) ->
    (set['u'] for set in data)

# return date_array in data
get_date_array = (data) ->
    (set['d'] for set in data)

# return the points as a string ready to feed into the <polygon>'s points attribute
get_points = (data, area=true) ->
    points = (get_point_string data[i], i for i in [0..data.length-1])
    if area
        points.unshift 0+","+graph_height()
        points.push graph_width()+","+graph_height()
    return points.join " "

# returns the nth key of a dict
# TODO: Check if really needed
get_nth_key = (n) ->
    1
# Closure around load_day_report
generate_reportlink = (day) ->
    return ->
        load_day_report(day)

# Adds a dot to the graph
add_dot = (svg, count, data) ->
    circle = document.createElementNS svg.namespaceURI, 'circle'
    circle.setAttribute "cx", get_x_position count
    circle.setAttribute "cy", get_y_position data['u']
    circle.setAttribute "r", get_dot_radius()
    circle.setAttribute "stroke", "#aaff00"
    circle.setAttribute "stroke-width", 1
    circle.setAttribute "fill", "#111"
    circle.onclick = generate_reportlink(data['d'])
    svg.appendChild(circle)

# Generates the data dots 
generate_dots = (svg, data) ->
    add_dot svg, i, data[i] for i in [0..data.length-1]

# Initialize the graph
initialize_graph = () ->
    vals = get_user_array data
    svg = document.getElementById 'tc_graph'
    svg.setAttribute 'width', graph_width()
    sns = svg.namespaceURI
    polygon = document.createElementNS(sns, 'polygon')
    polygon.setAttribute "points", get_points(vals)
    polygon.setAttribute "fill", "url(#grad1)"
    svg.appendChild(polygon)
    generate_dots svg, data

# Load the report for a day
load_day_report = (day) ->
    if (typeof @XMLHttpRequest == "undefined")
        console.log 'XMLHttpRequestis undefined'
        @XMLHttpRequest = ->
            try
                return new ActiveXObject("Msxml2.XMLHTTP.6.0")
            catch error
            try
                return new ActiveXObject("Msxml2.XMLHTTP.3.0")
            catch error
            try
                return new ActiveXObject("Microsoft.XMLHTTP")
            catch error
            throw new Error("This browser does not support XMLHttpRequest.")
    req = new XMLHttpRequest()
    req.addEventListener 'readystatechange', ->
        if req.readyState is 4
            success_resultcodes = [200, 304]
            if req.status in success_resultcodes
                document.getElementById('reportcontent').innerHTML = req.responseText
    url = '/reports/'+day+'.html'
    req.open 'GET', url, true
    req.send null

# Load the most recent daily report
load_most_recent = (data) ->
    load_day_report get_date_array(data)[data.length-1]

initialize_graph(data)
load_most_recent(data)
