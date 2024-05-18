data = set()
				
				
data_ordered = []
with open('sasa_values.txt','r') as file:
	for line in file:
		parts = line.split(':')
		if (len(parts) == 2):
			first_col = float(parts[0].strip())
			sec_col = float(parts[1].strip())
			
			data_ordered.append([first_col,sec_col])
	data_ordered = sorted(data_ordered, key=lambda x: x[1])
		
for row in data_ordered:
	print(row)

