file_meminfo = open('/proc/meminfo', 'r')

for line in file_meminfo:
    linesplitted = line.split(':')
    if linesplitted[0] == 'MemTotal':
        print(linesplitted[1])
