# confusion matrix 

class confmatrix:
    def __init__(self,classname):
        self.classname = classname
        self.total = 0
        self.__true_label= 0
        self.__false_label = 0
        self.tp = 0
        self.fp = 0
        self.tn = 0
        self.fn = 0

    

    def __get_tf(self): 
        return self.__fp
    
    def __get_tn(self): 
        return self.__tn

    def get_accuracy(self):
        return (self.tp + self.tn)/ self.total

    def get_error_rate(self):
        return 1 - self.get_accuracy() 

    def get_precision(self): 
        return self.tp /(self.tp + self.fp)

    def get_recall(self):
        return self.tp/(self.tp + self.fn)
    
    def get_sensitivity(self):
        return self.tp/(self.tp + self.fn)
    
    def get_specifitivy(self):
        return 1 - self.get_sensitivity()
