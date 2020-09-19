import pathlib, os, re, numpy
from pathlib import Path
from numpy import random
from essential_generators import DocumentGenerator

#-------------------Generate-Mininet---------------------------------------------------#

class Mininet:

    def __init__(self, name, path, size):
        self.name = name
        self.path = path
        self.size = size


    def createFiles(self):
        i=1
        while i<=self.size:
            f = open(str(self.path)+ '/' +str(i)+'.mnet', 'w')
            x=self.generate_content()
            f.write(str(x))
            f.close()
            i+=1


    def generate_content(self):
        x = random.randint(100)
        gen = DocumentGenerator()
        sen = ''
        while x >= 0:
            sen += str((gen.sentence()).encode("utf-8"))  + ' \n '
            x -= 1
        return sen



    def check_if_link_exist(self, list, link):
        for x in list:
            if link == x:
                return False
        return True

    def generate_links_p(self):
        link_list = list()
        link_in_page = list()
        num_of_import = int(self.size*0.1)
        num_of_mid = int(self.size*0.4)
        p = []
        counter = 1
        for i in range(self.size):
            if counter <= num_of_import:
                p.append(0.6/num_of_import)
                counter += 1
            elif counter <= (num_of_mid + num_of_import):
                p.append(0.2/num_of_mid)
                counter += 1
            else:
                p.append(0.2 / int(self.size*0.5))

        for file in Path(self.path).glob("*.mnet"):
            link_list.append(file)

        for file in Path(self.path).glob("*.mnet"):
            link_in_page = list()
            y = random.randint(self.size * 0.4)
            for i in range(y):
                x = numpy.random.choice(numpy.arange(0, self.size), p=p)
                if (self.check_if_link_exist(link_in_page, link_list[x])):
                    f = open(file, "a")
                    f.write('<< ' + str(link_list[x].name) + ' >>' + '\n')
                    f.close()
                    link_in_page.append(link_list[x])

            y = random.randint(self.size * 0.4)
            for i in range(y):
                x = numpy.random.choice(numpy.arange(0, self.size), p=p)
                if (self.check_if_link_exist(link_in_page, link_list[x])):
                    f = open(file, "r+")
                    random_lines = random.choice(f.readlines())
                    f.write('<< ' + random_lines + ' || ' + str(link_list[x].name) + '>>' + '\n')
                    f.close()
                    link_in_page.append(link_list[x])


    def generate_links(self, kind):
        link_list = list()
        link_in_page = list()

        if  kind == 1:
            range = self.size * 0.4 + 1
        elif kind == 2:
            range = self.size * 0.4

        for file in Path(self.path).glob("*.mnet"):
            link_list.append(file)

        for file in Path(self.path).glob("*.mnet"):
            link_in_page = list()
            y = random.randint(range)
            for i in range(y):
                x = random.randint(self.size)
                if (self.check_if_link_exist(link_in_page, link_list[x])):
                    f = open(file, "a")
                    f.write('<< ' + str(link_list[x].name) + ' >>' + '\n')
                    f.close()
                    link_in_page.append(link_list[x])

            y = random.randint(range)
            for i in range(y):
                x = random.randint(self.size)
                if (self.check_if_link_exist(link_in_page, link_list[x])):
                    f = open(file, "r+")
                    random_lines = random.choice(f.readlines())
                    f.write('<< '+ random_lines +' || ' + str(link_list[x].name) + '>>' + '\n')
                    f.close()
                    link_in_page.append(link_list[x])


def generate_mininet(net_path, size, extra_params=None):
    miniNet1 = Mininet('test', net_path, size )
    choise = False

    miniNet1.createFiles()

    print('What type of mininet you want to create?')
    print('1. Cyclic graph - Random links')
    print('2. A-Cyclic graph - Random links')
    print('3. Links divided to groups - importaint, medium and not importaint.')

    while choise is False:
        user_input = input()
        if user_input == '1':
            miniNet1.generate_links(user_input)
            choise = True
        elif user_input == '2':
            miniNet1.generate_links(user_input)
            choise = True
        elif user_input == '3':
            miniNet1.generate_links_p()
            choise = True
        else:
            print('Invalid choice, pick again')


    return miniNet1


#----------------------------Load-Mininet---------------------------------------------------#

class Load_Mininet:
    def __init__(self, net_pat, links_from_page,links_to_page, mininet_graph):
        self.net_pat = net_pat
        self.links_from_page = links_from_page
        self.links_to_page = links_to_page
        self.mininet_graph = mininet_graph



def get_links_from_file(file):
    f = open(file, "r")
    text = f.read()
    result = re.findall('<<(.*)>>', text)
    return result


def convert_to_graph(dict):
    graph = {}

    for key in dict:
        new_vals = list()
        for x in dict[key]:
            for w in x.split("|"):
                if w.endswith('.mnet'):
                    new_vals.append(w)
        graph.setdefault(key, new_vals)
    return graph


def get_links_to_page(G):
    links_to_page = {}
    for key in G:
        link_list = []
        for x in G:
            for y in G[x]:
                res = y.replace("|"," ").split()
                for w in res:
                    if key == w :
                        link_list.append(x)
        links_to_page.setdefault(key, link_list)
    return links_to_page



def load_mininet(net_path):
    files_list = net_path.glob('*.mnet')
    links_from_page = {}
    links_to_page = {}
    mininet_graph = {}

    for x in files_list:
        links = []
        links = get_links_from_file(x)
        links_from_page.setdefault(x.name, links)

    mininet_graph = convert_to_graph(links_from_page)
    links_to_page = get_links_to_page(links_from_page)
    loaded_mininet = Load_Mininet(net_path, links_from_page, links_to_page, mininet_graph)

    return loaded_mininet


#----------------------------------TEST && INSPECT--------------------------------------------------------#

