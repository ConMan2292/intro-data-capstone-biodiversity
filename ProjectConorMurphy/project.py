import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import chi2_contingency

# Load data
species = pd.read_csv('species_info.csv')

#print(species.head())

# Initial information checks.
species_count = species.scientific_name.nunique()
print(species_count)

species_type = species.category.unique()
print(species_type)

conservation_statuses = species.conservation_status.unique()

# Group conservation status' into another dataframe to make it more readible.
conservation_counts = species.groupby('conservation_status').scientific_name.nunique().reset_index()

#print conservation_counts

# Plot a chart before filling in NANs. This is to show in species under watch.
protection_counts1 = species.groupby('conservation_status')\
    .scientific_name.nunique().reset_index()\
    .sort_values(by='scientific_name')
    
plt.figure(figsize=(10, 4))
ax = plt.subplot()
plt.bar(range(len(protection_counts1)),protection_counts1.scientific_name.values)
ax.set_xticks(range(len(protection_counts1)))
ax.set_xticklabels(protection_counts1.conservation_status.values)
plt.ylabel('Number of Species')
plt.title('Conservation Status by Species')
labels = [e.get_text() for e in ax.get_xticklabels()]
plt.show()


# Fill NANs with a value so it can be more easily quantified.
species.fillna('No Intervention', inplace = True)

conservation_counts_fixed = species.groupby('conservation_status').scientific_name.nunique().reset_index()

print(conservation_counts_fixed)

protection_counts = species.groupby('conservation_status')\
    .scientific_name.nunique().reset_index()\
    .sort_values(by='scientific_name')

plt.figure(figsize=(10, 4))
ax = plt.subplot()
plt.bar(range(len(protection_counts)),protection_counts.scientific_name.values)
ax.set_xticks(range(len(protection_counts)))
ax.set_xticklabels(protection_counts.conservation_status.values)
plt.ylabel('Number of Species')
plt.title('Conservation Status by Species')
labels = [e.get_text() for e in ax.get_xticklabels()]
plt.show()

# Split the data into two categories: protected and not protected.
species['is_protected'] = species.conservation_status != 'No Intervention'

category_counts = species.groupby(['category', 'is_protected']).scientific_name.nunique().reset_index()

# Create a pivot table for nice viewing.
category_pivot = category_counts.pivot(columns='is_protected',
                      index='category',
                      values='scientific_name')\
                      .reset_index()
  
category_pivot.columns = ['category', 'not_protected', 'protected']

# Calculate the percentage of protected species in each category.
category_pivot['percent_protected'] = category_pivot.protected / (category_pivot.protected + category_pivot.not_protected)

print(category_pivot)

# Chi-squared test. Create contingency tables for the specific categories.
contingency = [[30, 146],
              [75, 413]]

pval_bird_mammal = chi2_contingency(contingency)[1]
print(pval_bird_mammal)
# No significant difference because pval > 0.05.

contingency_reptile_mammal = [[30, 146],
                              [5, 73]]

pval_reptile_mammal = chi2_contingency(contingency_reptile_mammal)[1]
print(pval_reptile_mammal)
# Significant difference! pval_reptile_mammal < 0.05.

# Foot & Mouth experiment. Read in new data set.
observations = pd.read_csv('observations.csv')

# Isolate sheep and they are the only animal of cencern in this test.
species['is_sheep'] = species.common_names.apply(lambda x: 'Sheep' in x)

species_is_sheep = species[species.is_sheep]

print(species_is_sheep)

sheep_species = species[(species.is_sheep) & (species.category == 'Mammal')]

print(sheep_species)

# Join the dataframe of only sheep species with observations.
sheep_observations = sheep_species.merge(observations)

print(sheep_observations.head())

# Group the observations by park for readibility and for charting..
obs_by_park = sheep_observations.groupby('park_name').observations.sum().reset_index()

print(obs_by_park)

fig = plt.figure(figsize=(16,4))
ax = plt.subplot()
plt.bar(range(len(obs_by_park)), obs_by_park.observations.values)
ax.set_xticks(range(len(obs_by_park)))
ax.set_xticklabels(obs_by_park.park_name.values)
plt.ylabel('Number of Observations')
plt.title('Observations of Sheep per Week')
plt.show()

# Sample size determination

baseline = 15
minimum_detectable_effect = 100*5/baseline
print(minimum_detectable_effect)

sample_size_per_variant = 890

yellowstone_weeks_observing = float(sample_size_per_variant) / obs_by_park.observations[(obs_by_park.park_name == 'Yellowstone National Park')]
print(yellowstone_weeks_observing)
# 1.755424 weeks

bryce_weeks_observing = float(sample_size_per_variant) / obs_by_park.observations[(obs_by_park.park_name == 'Bryce National Park')]
print(bryce_weeks_observing)
# 3.56

great_smokey_mountains_observing = float(sample_size_per_variant) / obs_by_park.observations[(obs_by_park.park_name == 'Great Smoky Mountains National Park')]
print(great_smokey_mountains_observing)
# 5.973154 weeks

yosemite_observing = float(sample_size_per_variant) / obs_by_park.observations[(obs_by_park.park_name == 'Yosemite National Park')]
print(yosemite_observing)
# 3.156028 weeks