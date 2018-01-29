class  Student(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score
    def print_score(self):
        print('%s:%s' %(self.name, self.score))
    def panduan(self):
        if self.score >= 60:
            return print('%s,你及格了!' % self.name)
        elif self.score < 60 & self.score>= 1:
            return print('%s,你没及格'% self.name)
        elif self.score == 0:
            return print('%s,你考试了么' % self.name)
'''
bart = Student('Bart Simpson', 60)

print('bart.name =', bart.name)
print(bart.panduan())'''