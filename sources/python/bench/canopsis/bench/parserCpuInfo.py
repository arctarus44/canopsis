file_cpuinfo = open('/proc/cpuinfo', 'r')

number_of_core = 0
cpu_name = ''


for line in file_cpuinfo:
    linesplitted = line.split(':')
    if linesplitted[0] == 'processor\t':
        number_of_core += 1
    if linesplitted[0] == 'model name\t':
        cpu_name = linesplitted[1]




