import pandas as pd
import plotly.express as px

block_results = pd.read_csv('csv/block_results.csv')
balance_results = pd.read_csv('csv/balance_results.csv')
call_results = pd.read_csv('csv/call_results.csv')

block_results['Rank'] = block_results.groupby('batch_time_id')['time_to_execute'].rank(ascending=True)
balance_results['Rank'] = balance_results.groupby('batch_time_id')['time_to_execute'].rank(ascending=True)
call_results['Rank'] = call_results.groupby('batch_time_id')['time_to_execute'].rank(ascending=True)

block_results['batch_run_id'] = block_results['batch_time_id'].rank(ascending=True, method='min').astype(int)
balance_results['batch_run_id'] = balance_results['batch_time_id'].rank(ascending=True, method='min').astype(int)
call_results['batch_run_id'] = call_results['batch_time_id'].rank(ascending=True, method='min').astype(int)


fig = px.box(block_results,x='provider',  y='time_to_execute', title="w3.eth.get_block('latest')",log_y=True, hover_data='batch_run_id',
labels={'provider': 'blockchain node provider', 'time_to_execute': 'time to execute, s'})
fig.write_html('html/getblock.html')

fig = px.box(balance_results,x='provider',  y='time_to_execute', title="w3.eth.get_balance()",log_y=True, hover_data='batch_run_id',
labels={'provider': 'blockchain node provider', 'time_to_execute': 'time to execute, s'})
fig.write_html('html/getbalance.html')

fig = px.box(call_results,x='provider',  y='time_to_execute', title="w3.eth.call()",log_y=True, hover_data='batch_run_id',
labels={'provider': 'blockchain node provider', 'time_to_execute': 'time to execute, s'})
fig.write_html('html/ethcall.html')

block_results = block_results.groupby('provider')[['time_to_execute', 'Rank']].mean().reset_index()
block_results.rename(columns={'time_to_execute': 'avg time to execute method, s', 'Rank': 'avg place'}, inplace=True)
block_results = block_results.sort_values(by='avg place', ascending=True)
block_results.reset_index(drop=True, inplace=True)
block_results.to_html('html/block_results.html', index=False)
block_results.batch_time_id[0].to_html('html/time.html', index=False)
balance_results = balance_results.groupby('provider')[['time_to_execute', 'Rank']].mean().reset_index()
balance_results.rename(columns={'time_to_execute': 'avg time to execute method, s', 'Rank': 'avg place'}, inplace=True)
balance_results = balance_results.sort_values(by='avg place', ascending=True)
balance_results.reset_index(drop=True, inplace=True)
balance_results.to_html('html/balance_results.html', index=False)

call_results = call_results.groupby('provider')[['time_to_execute', 'Rank']].mean().reset_index()
call_results.rename(columns={'time_to_execute': 'avg time to execute method, s', 'Rank': 'avg place'}, inplace=True)
call_results = call_results.sort_values(by='avg place', ascending=True)
call_results.reset_index(drop=True, inplace=True)
call_results.to_html('html/call_results.html', index=False)

concatenated_df = pd.concat([call_results, balance_results, block_results], ignore_index=True)
concatenated_df = concatenated_df.groupby('provider')[['avg time to execute method, s', 'avg place']].mean().reset_index()
concatenated_df = concatenated_df.sort_values(by='avg place', ascending=True)
concatenated_df.reset_index(drop=True, inplace=True)
concatenated_df.to_html('html/overall_results.html', index=False)

