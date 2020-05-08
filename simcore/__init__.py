# -*- coding: UTF-8 -*-
# member defination statement: empty string or zero for unnecessery user-operable variable;
# None with structure for user-inoperable variable;
# genereally, non-zero number need re-difination;
import os


class EvrSimSys:
    # system variable;
    AroCount=0
    AroList=[]
    AroRules=[]

    # rulesrelavant;
    def ruleCheck(self):
        pass
    # file relavant;
    def openSimFile(self,SimFileName):
        pass
    def deleteSimFile(self,SimFileName):
        pass
    def saveSimFile(self,SimFileName,SimFileContent,Replaceable=False):
        pass

    # Aro relavant;
    def getAro(self,index):
        'input int for AroID; str for AroName;'
        for aro in self.AroList:
            if type(index)==int:
                if aro.AroID==index: return aro
            elif type(index)==str:
                if aro.AroName==index: return aro
            else: return 'E: Parameter type error'
        return 'Error: Aro not found'

    def setAro(self,aroname,aroclass=None,**arokw):
        '''Arokw dict and Empty aroclass for modifing;
        Non-empty for creating;
        Para name must be the same with var name;'''
        ist=None
        if self.AroList!=[]:
            for aro in self.AroList:
                if aro.AroName==aroname:
                    ist=aro
                    break
        if ist is None:
            ist=aroclass(aroname)
            self.AroCount+=1
            ist.AroID=self.AroCount
            self.AroList.append(ist)
        for key in arokw:
            if hasattr(ist,key):
                setattr(ist,key,arokw[key])
        return ist

    def deleteAro(self,aroname):
        aro=self.getAro(aroname)
        if type(aro)==str: return aro
        self.AroList.remove(aro)
        if aroname in globals():
            del globals()[aroname]
        return


class Aro(object):
    AroID=None  # disturibute by sys;
    AroName="name"  # neccessery;
    AroDesc=''  # unneccessery, empty default;
    def __init__(self,aroname):
        self.AroName=aroname
        return
    def InitAro(self,**kw):
        self.AroName=kw['AroName']
        if 'AroDesc' in kw:
            self.AroDesc=kw['AroDesc']
        return


class AroSpace(Aro):
    SpaceSet=None   # AroID list;

    def setSpaceSet(self,aroname_list):
        'Accept Aroname string or list;'
        if self.SpaceSet is None:   # SpaceSet redifination;
            self.SpaceSet=[]
        if aroname_list is str:  # Para check;
            aroname_list=[aroname_list]
        for anl in aroname_list:    # Modify SpaceSet;
            if anl not in self.SpaceSet:
                self.SpaceSet.append(anl)
            else:
                self.SpaceSet.remove(anl)
        return

    def listSpaceSet(self):
        print(self.SpaceSet)
        return


class AroTimeSimulator(Aro):
    start_time=0
    end_time=0
    time_inter=0.1
    max_value_index=10
    min_value_index=-2

    def timeForward(self):
        return
    def timeBackward(self):
        return

# global;
ESS=EvrSimSys()
InitDict={'AroDesc':'Mainly Space.'}
space_Main=ESS.setAro('space_Main',AroSpace,**InitDict)
space_UI=ESS.setAro('space_UI',AroSpace)
space_Aro=ESS.setAro('space_Aro',AroSpace)

space_Main.setSpaceSet(['space_UI','space_Aro'])
