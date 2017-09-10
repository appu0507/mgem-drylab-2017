import sys

file = open(str(sys.argv[1]), "r+")
#argv[1] is a dereplicated fasta file
groups = []
sizes = []
group = ""

for line in file:
    line = line.strip()
    
    # Start of a new group
    if len(line) > 0 and line[0] == '>':
        groups.append(group)
        
        size = int(line[-2])
        sizes.append(size)
        
        group = ""
    
    group += line + "\n"
    
groups.append(group)

cnt = 0

for i in range(len(sizes)):
    if cnt > 10:
        break
    
    if 0 <= sizes[i] < 50:
        cnt += 1
        print(groups[i])
        
for i in range(len(sizes)):
    if cnt > 5:
        break
    
    if 50 <= sizes[i] < 100:
        cnt += 1
        print(groups[i])

for i in range(len(sizes)):
    if cnt > 5:
        break
    
    if 100 <= sizes[i] < 150:
        cnt += 1
        print(groups[i])

for i in range(len(sizes)):
    if cnt > 5:
        break
    
    if 150 <= sizes[i] < 200:
        cnt += 1
        print(groups[i])
    
for i in range(len(sizes)):
    if cnt > 5:
        break
    
    if 200 <= sizes[i] < 400:
        cnt += 1
        print(groups[i])
        
for i in range(len(sizes)):
    if cnt > 5:
        break
    
    if 400 <= sizes[i] < 1000:
        cnt += 1
        print(groups[i])
        
for i in range(len(sizes)):
    if cnt > 5:
        break
    
    if 1000 <= sizes[i] < 2000:
        cnt += 1
        print(groups[i])
        
for i in range(len(sizes)):
    if cnt > 5:
        break
    
    if 2000 <= sizes[i] < 10000:
        cnt += 1
        print(groups[i])
        
for i in range(len(sizes)):
    if cnt > 5:
        break
    
    if 10000 <= sizes[i]:
        cnt += 1
        print(groups[i])
