import pandas as pd

# see https://stackoverflow.com/a/70335285/
curr_ioc = pd.read_html('https://en.wikipedia.org/wiki/List_of_IOC_country_codes')[0].set_index('Code')['National Olympic Committee']
hist_ioc = pd.read_html('https://en.wikipedia.org/wiki/List_of_IOC_country_codes')[2].set_index('Code')['Nation/Team']
obs_ioc = pd.read_html('https://en.wikipedia.org/wiki/List_of_IOC_country_codes')[3].set_index('Code')['Nation (NOC)']
spec_ioc = pd.read_html('https://en.wikipedia.org/wiki/List_of_IOC_country_codes')[4]
spec_nations = list(spec_ioc['Nation/team'].values)
correct_spec_nations = []
for nation in spec_nations:
    if nation != 'Athletes from Kuwait':
        # remove the from after the actual country name...
        parts = nation.split(' ')
        try:
            from_idx = parts.index('from')
            parts = parts[:from_idx]
        except Exception as e:
            pass
        correct_spec_nations.append(' '.join(parts))
    else:
        correct_spec_nations.append(nation)
spec_ioc['Nation/team'] = correct_spec_nations
spec_ioc = spec_ioc.set_index('Code')['Nation/team']
ioc = pd.concat([curr_ioc, hist_ioc, obs_ioc, spec_ioc])
ioc.to_csv('all_ioc.csv')