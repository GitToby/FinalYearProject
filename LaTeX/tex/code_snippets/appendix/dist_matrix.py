from sklearn import metrics


def CD_map_to_int(x):
    # Returns D:0 C:1
    return 68 - ord(x)


# Itertuples is a list of (index,col1,col2,..) for each row. We sort them by score first
df_vectors = pd.DataFrame()
df_vectors_strings = pd.DataFrame()
df_generation_max = df_generation_max.sort_values('opponent_name')
df_generation_max = df_generation_max.sort_values('best_score')
for tup in df_generation_max.itertuples():
    # index vals mean the indexing starts at 1 so +1 to these:
    #(0, 'generation'), (1, 'score_mean'), (2, 'score_median'), (3, 'score_pop_var'), (4, 'score_range'), (5, 'best_score'), (6, 'best_sequence'), (7, 'opponent_name'), (8, 'seed'), (9, 'analysis_name'), (10, 'base_player'), (11, 'stochastic'), (12, 'memory_depth'), (13, 'makes_use_of'), (14, 'score_bin'), (15, 'start_move'), (16, 'num_blocks'), (17, 'mean_block_len'), (18, 'median_block_len')
    seq_str = tup[7]
    opponent_name = str(tup[8])
    best_score = tup[6]
    bins = tup[15]
    # Mapping to integers 0 &1
    df_vectors[opponent_name] = list(
        map(CD_map_to_int, seq_str)) + [best_score] + [seq_str] + [bins]

    # No Mapping Cs & Ds
    df_vectors_strings[opponent_name] = list(
        seq_str) + [best_score] + [seq_str] + [bins]


move_cols = ['move ' + str(x+1) for x in range(200)]
# Transposing and labeling moves as were forming it in a rotated way.
# (Its easier to just make 2 dfs than map one to the other)
df_vectors = df_vectors.transpose()
df_vectors.columns = move_cols + ["best_score", "best_sequence", "score_bins"]

df_vectors_strings = df_vectors_strings.transpose()
df_vectors_strings.columns = move_cols + \
    ["best_score", "best_sequence", "score_bins"]

# Manhatten Distance == Hamming Distance in this example
# Intresting examples: cosine(??), hamming, jaccard sim
dist_array_ham = metrics.pairwise.pairwise_distances(
    df_vectors[move_cols], metric='hamming')
# add labels
dist_array_ham = pd.DataFrame(
    dist_array_ham, index=df_vectors.index, columns=df_vectors.index)

dist_array_cos = metrics.pairwise.pairwise_distances(
    df_vectors[move_cols], metric='cosine')
dist_array_cos = pd.DataFrame(
    dist_array_cos, index=df_vectors.index, columns=df_vectors.index)

dist_array_jac = metrics.pairwise.pairwise_distances(
    df_vectors[move_cols], metric='jaccard')
dist_array_cos = pd.DataFrame(
    dist_array_cos, index=df_vectors.index, columns=df_vectors.index)

dist_array_other = metrics.pairwise.pairwise_distances(
    df_vectors[move_cols], metric='correlation')
dist_array_cos = pd.DataFrame(
    dist_array_cos, index=df_vectors.index, columns=df_vectors.index)
