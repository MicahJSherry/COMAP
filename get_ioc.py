import pandas as pd

def remove_code(names, exclude={}):
    new_names = []
    for name in names:
        if name not in exclude:
            parts = name.split(' ')
            try:
                from_idx = parts.index('code')
                parts = parts[:from_idx]
            except Exception as e:
                pass
            new_names.append((' '.join(parts)))
        else:
            new_names.append(name)
    return new_names

def remove_from(names, exclude={}):
    new_names = []
    for name in names:
        if name not in exclude:
            parts = name.split(' ')
            try:
                from_idx = parts.index('from')
                parts = parts[:from_idx]
            except Exception as e:
                pass
            new_names.append((' '.join(parts)))
        else:
            new_names.append(name)
    return new_names

def remove_From(names, exclude={}):
    new_names = []
    for name in names:
        if name not in exclude:
            parts = name.split(' ')
            try:
                from_idx = parts.index('From')
                parts = parts[:from_idx]
            except Exception as e:
                pass
            new_names.append((' '.join(parts)))
        else:
            new_names.append(name)
    return new_names

# see https://stackoverflow.com/a/70335285/
curr_ioc = pd.read_html('https://en.wikipedia.org/wiki/List_of_IOC_country_codes')[0]
curr_ioc['National Olympic Committee'] = remove_From(remove_from(remove_code(curr_ioc['National Olympic Committee'])))
curr_ioc = curr_ioc.set_index('Code')['National Olympic Committee']

hist_ioc = pd.read_html('https://en.wikipedia.org/wiki/List_of_IOC_country_codes')[2]
hist_ioc['Nation/Team'] = remove_From(remove_from(remove_code(hist_ioc['Nation/Team'])))
hist_ioc = hist_ioc.set_index('Code')['Nation/Team']

obs_ioc = pd.read_html('https://en.wikipedia.org/wiki/List_of_IOC_country_codes')[3]
obs_ioc['Nation (NOC)'] = remove_From(remove_from(remove_code(obs_ioc['Nation (NOC)'])))
obs_ioc = obs_ioc.set_index('Code')['Nation (NOC)']

spec_ioc = pd.read_html('https://en.wikipedia.org/wiki/List_of_IOC_country_codes')[4]
spec_ioc['Nation/team'] = remove_From(remove_from(remove_code(spec_ioc['Nation/team'].values), exclude=('Athletes from Kuwait')))
spec_ioc = spec_ioc.set_index('Code')['Nation/team']

special_cases = pd.DataFrame.from_dict({'Code':['TPE','TPE','CZE','CZE','IPP','MKD','CVD'], 'Nation':['Formosa','Taiwan','Czechia','Czech Republic','FR Yugoslavia','Macedonia','Cabo Verde']}).set_index('Code')['Nation']
ioc = pd.concat([curr_ioc, hist_ioc, obs_ioc, spec_ioc, special_cases])
ioc = ioc.drop_duplicates(keep='first')
ioc = ioc.rename('Nation')
ioc.to_csv('all_ioc.csv')