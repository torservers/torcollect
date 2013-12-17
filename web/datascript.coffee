data = [1,2,3,4,5,6]

graph_width = () -> return document.getElementById("graphspace").clientWidth
x_space_between_points = () -> return graph_width() / data.length
get_x_position = (count) -> return count * x_space_between_points()
y_space_between_points = () -> return graph_height() / maxim data
get_y_position = (value) -> return graph_height() - value * y_space_between_points()
graph_height = () -> 100
get_point_string = (value, count) -> return get_x_position(count)+","+get_y_position(value)

maxim = (data, i=0) ->
    if i+1 == data.length
        return Math.max(-Infinity,data[i])
    else
        return Math.max(data[i],maxim data, i+1)

get_points = (data) ->
    points = [get_point_string data[i], i for i in [0..data.length]]
    return points.join " "

initialize_graph = () ->
    svg = document.createElement('svg')
    sns = svg.namespaceURI
    polygon = document.createElement(sns, 'polygon')
    polygon.setAttribute "points", get_points(data)
    polygon.setAttribute "fill", "#ffffff"
    svg.appendChild(polygon)
    document.getElementById("graphspace").appendChild(svg)
initialize_graph()
