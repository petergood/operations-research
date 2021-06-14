import networkx as nx
import matplotlib.pyplot as plt
import pandas

def draw_trace(selected_orders, trace):
    G = nx.DiGraph()
    colors = []
    orders_map = {}

    for i in range(len(selected_orders)):
         _, _, pickup_point, drop_point = selected_orders[i]
         orders_map[pickup_point] = {"color": "blue", "label": str(i) + "/0"}
         orders_map[drop_point] = {"color": "green", "label": str(i) + "/1"}

    for o in orders_map:
        G.add_node(orders_map[o]["label"], pos=o)
        colors.append(orders_map[o]["color"])

    for i in range(len(trace)):
        if i != 0:
            G.add_edge(orders_map[trace[i-1][0]]["label"], orders_map[trace[i][0]]["label"])
    G.add_edge(orders_map[trace[len(trace)-1][0]]["label"], orders_map[trace[len(trace)-1][1]]["label"])

    pos=nx.get_node_attributes(G,'pos')

    nx.draw(G, pos, edge_color='red', node_color=colors, with_labels=True)
    plt.legend()
    plt.show()

def draw_charts(input_file):
    df = pandas.read_csv(input_file)
    df.insert(0, 'vertex_count', range(5, len(df)+5))
    ax = df.plot(x = 'vertex_count', y='ABC')
    df.plot(ax = ax, x = 'vertex_count', y='ASO')
    plt.show()
    print(df)

draw_charts('result.csv') 
