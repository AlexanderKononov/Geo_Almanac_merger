def getCellLineGEO(name_GEOfile):
    smpls = {}
    f_w = open(name_GEOfile, 'r')
    line = f_w.readline()
    while line != '':
        if i[0] != '!':
            break
        l = line.strip().split(' = ')
        if l[0].find('subset_description') != -1:
            l2 = f_w.readline().strip().split(' = ')
            smpls[l[1].strip()] = l2[1].strip().split(',')
            line = f_w.reedline()
            continue
        line = f_w.reedline()
    f_w.close()
    return smpls

def getGeneName(name_GEOfile):
    geneName =[]
    f_w = open(name_GEOfile, 'r')
    line = f_w.readline()
    while line.find('dataset_table_begin') == -1:
        line = f_w.readline()
    line = f_w.readline()
    line = f_w.readline().strip()
    while line != '!dataset_table_end' or line != '':
        geneName.append(line.split('\t')[1].strip())
    f_w.close()
    return geneName


def getGEOData(name_GEOfile, smpl):
    f_w = open(name_GEOfile, 'r')
    smpl_coordinates = {}
    data_tmp = []
    data = []
    cell_name = []
    line = f_w.readline().strip()
    while line.find('dataset_table_begin') == -1:
        line = f_w.readline().strip()
    line = f_w.readline().strip().split('\t')
    for i in smpl.keys:
        cell_name.append(i)
        smpl_coordinates[i] = []
        for j in range(len(line)):
            if line[j].strip() in smpl[i]:
                smpl_coordinates[i].append(j)

    line = f_w.readline().strip()
    while line != '!dataset_table_end' or line != '':
        l = line.split('\t')
        data_tmp.append(l)
        line = f_w.readline().strip()
    f_w.close()

    cell_name_all =[]
    for i in smpl_coordinates.keys:
        for j in range(len(smpl_coordinates[i])):
            line = [i + '.' + str(j)]
            for k in data_tmp:
                line.append(k[smpl_coordinates[i][j]])
            data.append(line)
    return data, cell_name




def scoreCompresser(list_of_score):
    if max(list_of_score) > -1 * min(list_of_score):
        score = max(list_of_score)
    else:
        score = min(list_of_score)

def getAlmanacData(name_Almanac_data,  drugA = '752', drugB = '3088'):
    colomns = {}
    cell_line = {}
    cell_name = set()
    data = {}
    f_w = open(name_Almanac_data, 'r')
    line = f_w.readline().strip().split(',')
    c=0
    for i in line:
        colomns[i] = c
        c+=1
    line = f_w.readline().strip()
    while line != '':
        l = line.split(',')
        if (l[colomns['NSC1']] != drugA and l[colomns['NSC1']] != drugB) or (l[colomns['NSC2']] != drugA and l[colomns['NSC2']] != drugB):
            line = f_w.readline()
            continue
        if l[colomns['CELLNAME']] in cell_name:
            cell_line[l[colomns['CELLNAME']]].append(l[colomns['SCORE']])
        else:
            cell_name.add(l[colomns['CELLNAME']])
            cell_line[l[colomns['CELLNAME']]] = [l[colomns['SCORE']]]
        line = f_w.readline()
    score = 0
    for name in cell_name:
        data[name] = scoreCompresser(cell_line[name])
    f_w.close()
    return data, cell_name

def nameConverter(GEO_names, Almanac_name):
    converter = {}
    flag = False
    for g_name in GEO_names:
        g_parts = re.split('[_/-]' , g_name.strip())
        for a_name in Almanac_name:
            for g in g_parts:
                if a_name.find(g.strip().strip('_').strip('/').strip('-')) == -1:
                    flag = False
                    break
                else:
                    flag = True
            if flag:
                flag = False
                converter[g_name] = a_name
                break
    return  converter

def mergingData(GEO_data, Almanac_data, converter):
    data =[]
    for i in GEO_data:
        line = [i]
        line.append(Almanac_data[converter[i[0].split('.')[0]]])
        data.append(line)
    return data

def writingData(mergingData, geneNames):
    f_w = open ('out_file.csv', 'w'):
    f_w.write('Cell_line,')
    for i in geneNames:
        f_w.write(i + ',')
    f_w.write('Score\n')
    for i in mergingData:
        for j in i:
            f_w.write(j + ',')
            f_w.write('\n')
    f_w.close()