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

#delays the execution of a function
delay = (time, f) -> setTimeout f, time

# return user_array in data
get_user_array = (data) ->
    (set['u'] for set in data)

# return date_array in data
get_date_array = (data) ->
    (set['d'] for set in data)

# returns an array of one specific attribute from a list of objects
# if more that one attributes is given, the chosen attributes will be summed up
get_attribute_array = (data, attributes) ->
    ((set[attribute] for set in data) for attribute in attributes).reduce (x,y) ->
        (x[i]+y[i] for i in  [0..x.length-1])

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
                delay 1000, -> m_generate_traffic_graphs()
                
    url = '/reports/'+day+'.html'
    req.open 'GET', url, true
    req.send null

# Load the most recent daily report
load_most_recent = (data) ->
    load_day_report get_date_array(data)[data.length-1]

initialize_graph(data)
load_most_recent(data)


###################################
# Minigraphs
###################################

# Returns the graphs width. It is being read from the element that
# the graph will be displayed in. This element is passed via it's dom-ID
m_graph_width = (id) ->
    return document.getElementById(id).offsetWidth

# Returns the graphs height. It is being read from the element that
# the graph will be displayed in. The element is passed via it's dom-Id
m_graph_height = (id) ->
    return document.getElementById(id).offsetHeight

# Returns the space between two points on the x-axis in a graph.
# The x-point-distance is being calculated based on how many data-objects
# are in the data array that is to be displayed
m_x_space_between_points = (id, data) ->
    return m_graph_width(id) / (data.length - 1)

# Returns the space (in px) per step on the scale of the data contained in the list.
# attributes should contain a set of attributes found in the data-objects that are to
# be taken into account.
# E.G. when you have a list that contains objects that has an attribute 's' that you want
# to display, you pass ('s') in attributes. if you want two or more attributes that should
# be displayed in the graph together, you can do so, too
m_y_space_between_points = (id, data, attributes) ->
    return (m_graph_height(id) - get_dot_radius()*2) / maxim get_attribute_array data, attributes

# Returns the X-position of a point
m_get_x_position = (id, data, count) ->
    return Math.round count * m_x_space_between_points(id, data)

# Returns the y position of a value
m_get_y_position = (id, data, attributes, value) ->
    return Math.round m_graph_height(id) - value * m_y_space_between_points(id, data, attributes) + get_dot_radius()

m_get_point = (id, data, abs_attributes, count, value) ->
    return m_get_x_position(id, data, count)+","+m_get_y_position(id, data, attributes, value)

m_get_points = (id, data, attribute, abs_attributes, area=true) ->
    points = (get_point get_attribute_array(data, attribute)[i], i for i in [0..data.length-1])
    if area
        points.unshift 0+","+m_graph_height(id)
        points.push m_graph_width(id)+","+m_graph_height(id)
    return points.join " "

m_generate_received_polygon = (id, traffic_data) ->
    svg_ns = "http://www.w3.org/2000/svg"
    polygon = document.createElementNS svg_ns, 'polygon'
    polygon.setAttribute 'points', m_get_points(id, traffic_data, 'r', ['r','s'])
    polygon.setAttribute 'fill', '#00f'
    return polygon

m_generate_sent_polygon = (id, traffic_data) ->
    svg_ns = "http://www.w3.org/2000/svg"
    polygon = document.createElementNS svg_ns, 'polygon'
    polygon.setAttribute 'points', m_get_points(id, traffic_data, 's', ['r','s'])
    polygon.setAttribute 'fill', '#f00'
    return polygon

m_get_left = (element) ->
    if element.parentNode == document.body
        return element.offsetLeft
    else
        return m_get_left element.parentNode + element.offsetLeft

m_get_top = (element) ->
    if element.parentNode == document.body
        return element.offsetTop
    else
        return m_get_top element.parentNode + element.offsetTop

# generate the trafficgraph for a tablerow
m_generate_traffic_graph = (id) ->
    svg_ns = "http://www.w3.org/2000/svg"
    svg = document.createElementNS svg_ns, 'svg'
    tr = document.getElementById id
    svg.setAttribute 'width', tr.offsetWidth
    svg.setAttribute 'height', tr.offsetHeight
    traffic_data = brg_traffic_data[id.split("_")[1].toString()]
    svg.appendChild m_generate_received_polygon id, traffic_data
    svg.appendChild m_generate_sent_polygon id, traffic_data
    document.body.appendChild svg
    svg.style.display = "block"
    svg.style.position = "absolute"
    svg.style.top = m_get_top(tr)+"px"
    svg.style.left = m_get_left(tr)+"px"
    svg.style.zIndex = -1

m_generate_traffic_graphs = () ->
    (generate_traffic_graph "brgl_"+id for id in keys brg_traffic_data)
    
