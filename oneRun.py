f = open('BCrun.txt')
new = open('MAElist.txt','w+')
current = f.readline().replace('\n','')
while (current != ''):
    if current == 'days_to_last_follow_up':
        new.write(current+'\n')
        current = f.readline().replace('\n','')
        while(current != '' and current != 'simple_somatic_mutations'):
            current = current.replace('([','').replace(']','').replace(')','').replace(' ','')
            current = current.split(',')
            new.write(current[6]+'\n')
            current = f.readline().replace('\n','')
    else:
        current = f.readline().replace('\n','')
