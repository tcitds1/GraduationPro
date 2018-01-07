class Robot:
    robotCount = 0;
    def __init__(self, name):
        self.name = name
        Robot.robotCount += 1
        print('the robot name is {0}'.format(self.name))
    def die(self):
        print('the robot {0} died'.format(self.name))
        Robot.robotCount -= 1
    def sayHi(self):
        print(self.name + ' say hello')

    @classmethod
    def howmany(cls):
        print(cls.robotCount)

rb1 = Robot('luozhixiang')
rb1.sayHi()
rb1.die()

rb2 = Robot('ywx')
print('there are {0} robot'.format(Robot.robotCount))