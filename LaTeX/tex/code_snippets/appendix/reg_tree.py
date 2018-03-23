# We use mean absolut error, as we want to penalise the magnitude of the error linearly 
# (rmse would how how the variance in our scores is reduced move by move)
regressor_tree = tree.DecisionTreeRegressor(criterion='mae',max_depth=4)
#Rerun this for # of cs in a sequence.
regressor_tree.fit(df_vectors[move_cols],df_vectors["best_score"],)

# This will export the graph to a .dot file, use `dot -Tpng .\tree.dot -o tree.png` in cmd to convert to png
# dot_data_clasif = tree.export_graphviz(regressor_tree, out_file='tree.dot') 
dot_data_reg = tree.export_graphviz(regressor_tree, out_file='reg_tree.dot') 
# Run on CMD line
!dot -Tpng .\reg_tree.dot -o reg_tree.png
!dot -Tpdf .\reg_tree.dot -o reg_tree.pdf

i = Image.open('./reg_tree.png')
plt.figure(figsize=(20,20))
plt.imshow(i)