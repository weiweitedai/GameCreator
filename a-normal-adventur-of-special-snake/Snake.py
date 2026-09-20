import Constant as c
import Game
#蛇类
class Snake:
    def __init__(self):
        start_x = c.GRID_WIDTH // 2
        start_y = c.GRID_HEIGHT // 2  
        self.head = (start_x, start_y)
        self.body = [(start_x - i, start_y) for i in range(0, 3)]  # 初始身体长度为3
        self.direction = c.RIGHT
        #self.next_direction = RIGHT 使用单格缓冲会出现卡连招丢键的情况
        self.pending = [] #通过队列原理，控制长度最大为2保证连招存在，手感丝滑
        #这个算新版本吧
        self.prev_body = None 
        self.grow_flag = False

    def move(self):
        self.direction = self.pending.pop(0) if self.pending else self.direction
        self.prev_body = self.body.copy()
        old_head = self.head
        new_head = ((old_head[0] + self.direction[0]) % c.GRID_WIDTH, (old_head[1] + self.direction[1]) % c.GRID_HEIGHT)

        #判断是否撞墙
        '''
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            return False  # 撞墙，游戏结束
        '''
        #判断是否撞到自己
        if self.grow_flag:
             body_to_check = self.body[1:]
        else:
             body_to_check = self.body[1:-1]
        if new_head in body_to_check:  # 排除头部
            return False  # 撞到自己，游戏结束

        #更新身体
        self.head = new_head
        self.body.insert(0, new_head)  #将新头部插入身体列表的开头
        if not self.grow_flag:
            self.body.pop()  #移除尾部
        else:
            self.grow_flag = False  #重置增长标志

        return True  # 移动成功

    def grow(self):
        self.grow_flag = True

    def change_direction(self, new_direction):
        last = self.pending[-1] if self.pending else self.direction

        if (new_direction[0] * -1, new_direction[1] * -1) != last and new_direction != last :  #防止180度转向
            if len(self.pending) < 2:
                 
                self.pending.append(new_direction)