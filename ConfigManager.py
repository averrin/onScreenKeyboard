__author__ = 'tsa'
import re
import ConfigParser

def ConfigSectionMap(Config,section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


class ConfigManager():
    def __init__(self,filename):
        self._readProgConfigFromFile(filename)
        self.numOfLangs=len(self.index_to_key_name_dict[self.index_to_key_name_dict.keys()[0]])/2

    def _readProgConfigFromFile(self,path_to_file):
        configParser = ConfigParser.ConfigParser()
        configParser.read(path_to_file)

        self.sections = [str(val) for val in configParser.sections()]
        self.filename = str(ConfigSectionMap(configParser, "KEYBOARD SETTINGS")['keyboard_conf_file'])
        self.font_name = str(ConfigSectionMap(configParser, "KEYBOARD SETTINGS")['font_name'])

        self.font_size = int(ConfigSectionMap(configParser, "KEYBOARD SETTINGS")['buttons_font_size'])

        self.shift_keys=set()
        for my_str in str(ConfigSectionMap(configParser, "KEYBOARD SETTINGS")['keyboard_shift_keys']).split(','):
            if my_str!='':
                self.shift_keys.add(int(my_str))

        self.bold_underscored_keys=set()
        for my_str in str(ConfigSectionMap(configParser, "KEYBOARD SETTINGS")['keyboard_bold_underscored_keys']).split(','):
            if my_str!='':
                self.bold_underscored_keys.add(int(my_str))
        self.createConfigFromFile(self.filename)

        if "KEYBOARD SETTINGS" in self.sections:
            sticky_key=ConfigSectionMap(configParser, "KEYBOARD SETTINGS")['sticky_key_behaviour']
            if sticky_key=='1' or sticky_key=='True' or sticky_key=='true':
                self.sticky_key_behaviour = True
            else:
                self.sticky_key_behaviour = False
        else:
            self.sticky_key_behaviour = False

        if "WINDOW MANAGER" in self.sections:
            unity_is_wm=ConfigSectionMap(configParser, "WINDOW MANAGER")['unity']
            if unity_is_wm=='1' or unity_is_wm=='True' or unity_is_wm=='true':
                self.wm_is_unity = True
            else:
                self.wm_is_unity = False
        else:
            self.wm_is_unity = False

        if "MAIN" in self.sections:
            debug=ConfigSectionMap(configParser, "MAIN")['debug']
            if debug=='1' or debug=='True' or debug=='true':
                self.debug = True
            else:
                self.debug = False
        else:
            self.debug = False

        self.colored_keys=dict()
        if "KEYBOARD SETTINGS" in self.sections:
            if 'colored_group' in ConfigSectionMap(configParser, "KEYBOARD SETTINGS"):
                self.keys_are_colored=True
                with open(path_to_file) as f:
                    lines=f.readlines()
                for line in lines:
                    if 'colored_group' in line:
                        splitted_line=line.strip('\n')[line.find('colored_group')+14:].split(',')
                        group_color=splitted_line[0]
                        group_keys=splitted_line[1:]
                        for key in group_keys:
                            self.colored_keys[int(key)]=group_color

    def getKeyNameFromStr(self,my_str):
        processed_str=my_str[my_str.find(":")+2:my_str.rfind(":")-1]
        result_name=processed_str[0]
        result_list=[]
        for index in xrange(1,len(processed_str)):
            if processed_str[index]==',':
                if result_name=='':
                    result_name=","
                else:
                    result_list.append(result_name)
                    result_name=""
            else:
                result_name+=processed_str[index]
        if result_name!='':
            result_list.append(result_name)
        return result_list

    def getKeyName(self,key_index,keyboard_shift,keyboard_lang):
        return self.index_to_key_name_dict[key_index][keyboard_shift*1+keyboard_lang*self.numOfLangs]

    def getKeyPosFromStr(self,my_str):
        processed_str=my_str[my_str.rfind(":")+1:]
        result_list=[]
        for pos in processed_str.split(','):
            result_list.append(int(pos))
        return result_list

    def createConfigFromFile(self,filename):
        self.index_to_key_name_dict=dict()
        self.index_to_key_pos=dict()
        self.key_pos_to_index=dict()

        self.keys_in_row=dict()
        if '~' in filename:
            from os.path import expanduser
            home = expanduser("~")
            filename=filename.replace("~",home)
        with open(filename) as f:
            lines=f.readlines()
        lines=lines[1:]

        self.numOfRows=1

        for line in lines:
            line = re.sub('\n\t ', '', line)
            if line!='':
                splitted_line=line.split(':')
                self.index_to_key_name_dict[int(splitted_line[0])]=self.getKeyNameFromStr(line)
                position=self.getKeyPosFromStr(line)
                self.index_to_key_pos[int(splitted_line[0])]=position
                self.key_pos_to_index[tuple(position)]=int(splitted_line[0])
                if position[0] not in self.keys_in_row:
                    self.keys_in_row[position[0]]=[position[1]]
                else:
                    self.keys_in_row[position[0]].append(position[1])
                if position[0]>self.numOfRows:
                    self.numOfRows=position[0]

    def getNumOfRows(self):
        return self.numOfRows

    def getNumOfKeysInRow(self,row_num):
        if row_num in self.keys_in_row:
            return len(self.keys_in_row[row_num])
        else:
            return 0