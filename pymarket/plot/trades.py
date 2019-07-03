import networkx as nx
import matplotlib.pyplot as plt


def plot_trades_as_graph(bids, transactions, ax):
    """
    Plots all the bids as a bipartit graph
    with buyers and trades and an edge between
    each pair that traded

    Parameters
    -----------
    transactions (pandas dataframe):
        Transactions table with the result of running the market
    bids (pandas dataframe):
        Bids table with the submitted bids to the market
    ax (matplotlib.pyplot axes):
        axe in which to plot, if None, create new

    Returns:
    ax (matplotlib figure):
        axe in which everything is plotted
    """
    bids = bids.get_df()
    tmp = transactions.get_df()
    tmp['user_1'] = tmp.bid.map(bids.user)
    tmp['user_2'] = tmp.source.map(bids.user)
    tmp['buying'] = tmp.bid.map(bids.buying)
    buyers = bids.loc[bids['buying']].index.values

    G = nx.from_pandas_edgelist(tmp, 'user_1', 'user_2')

    edge_labels = {}
    duplicated_labels = tmp.set_index(
        ['user_1', 'user_2'])['quantity'].to_dict()
    for (x, y), v in duplicated_labels.items():
        if ((x, y) not in edge_labels and (y, x) not in edge_labels):
            edge_labels[(x, y)] = v

    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))

    pos = nx.bipartite_layout(G, buyers, align='horizontal', scale=3)
    _ = nx.draw_networkx_nodes(
        G,
        pos=pos,
        ax=ax,
        node_color='k',
        node_size=500)
    _ = nx.draw_networkx_labels(G, pos=pos, ax=ax, font_color='w')
    _ = nx.draw_networkx_edges(G, pos=pos, label=G, ax=ax)
    _ = nx.draw_networkx_edge_labels(
        G,
        pos=pos,
        edge_labels=edge_labels,
        label_pos=0.9,
        ax=ax)
    _ = ax.axis('off')

    return ax