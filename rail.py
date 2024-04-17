import osmnx as ox
ox.config(log_console=True, use_cache=True)
my_custom_filter = '["railway"]'
G = ox.graph_from_point((51.5073509,-0.1277583), 
                        infrastructure = 'way["railway"~"rail"]',
                        network_type = 'none',
                        custom_filter = my_custom_filter
                        )

ox.plot_graph(G)