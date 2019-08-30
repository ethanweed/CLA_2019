def POS (pathin, file):
    import os
    from string import punctuation as p


    os.chdir(pathin)

    removelist = ['\t', '\r']


    with open(file,'r') as f:
        text = f.read()
        for item in removelist:
            text = text.replace(item, '')
        text = text.split('@')

        #print(text)

    for line in text:
        if line.startswith('Participants:'):
            p = line.replace('Participants:', '')
            p = p.split(',')

        p1 = []
        for i, val in enumerate(p):
            v1 = val.replace(' ','')
            v2 = v1.replace('\n', '')
            p1.append(v2[0:3])
        people = p1
        

    #with open(file,'r') as f:
     #   text = f.read()
      #  for item in removelist:
       #     text = text.replace(item, '')
        #text = text.split('\n')

        trans = []
        for line, val in enumerate(text):
        	if val.startswith('%mor') and text[line-1][1:4] in people:
              trans.append(text[line-1])
              trans.append(val)

            #label = val[1:4]
            #if label in people and text[line+1].startswith('%mor'):
             #   trans.append(val)
              #  trans.append(text[line+1])
            #elif label == 'mor':
                #trans.append(val)


    grouped = [trans[n:n+2] for n in range(0, len(trans), 2)]


    p = '.!?'

    turn = []
    speaker = []
    mor = []
    for i, val in enumerate(grouped):
        turn.append(i+1)


    for i in grouped:
        s = i[0]
        m = i[1]
        for c in p:
            m = m.replace(c, '')
            m = m.strip()
            m = m.replace('%mor:', '')
            speaker.append(s[1:4])
            mor.append(m)

    z = list(zip(turn, speaker, mor))


    turn = []
    speaker = []
    pss = []

    for i, val in enumerate(z):
        x = z[i]
        t = x[0]
        s = x[1]
        m = x[2]
        m = m.split(' ')
        p = []
        #w = []
        for n in m:
            temp = n.split('|')
            p.append(temp[0])
            #w.append(temp[1])
        turn.append(t)
        speaker.append(s)
        pss.append(p)
        #wds.append(w) 
    pw = list(zip(turn,speaker,pss))


    lines = []
    for i in pw:
        num = str(i[0])
        speaker = i[1]
        #wds = i[3]
        pss = i[2]
        for j, val in enumerate(pss):
            p = pss[j]
            #w = wds[j]
            #temp = num + ',' + speaker + ',' + w + ',' + p + '\n'
            temp = num + ',' + speaker + ',' + p + '\n'
            temp = num + ',' + speaker + ',' + ',' + p + '\n'
            temp = num + ',' + speaker + ',' + p + '\n'
            lines.append(temp)      

    #header = 'Turn,' + 'Speaker,' + 'Word' + 'POS' + '\n'
    header = 'Turn,' + 'Speaker,' + 'POS' + '\n'
    data = ''.join(lines)
    output = header + data
    return(output)