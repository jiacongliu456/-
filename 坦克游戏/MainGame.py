# 独特的设计，创新点在哪里
import sys, pygame, time, random, scene, Home

_display = pygame.display
# 加三个道具，一个是子弹速度的道具，一个是坦克速度的道具

Window_width = 630
Window_height = 630
# Color也是pygame的一个对象
COLOR_BLACK = pygame.Color(0, 0, 0)
COLOR_RED = pygame.Color(255, 0, 0)
COLOR_WHITE = pygame.Color(255, 255, 255)
# SPEED = 18
# 我方坦克速度
Mytank_speed = 3
addTankSpped = 1
# 子弹速度
Bullet_speed = 3
# 子弹每次加速的速度
addBulletSpeed = 1
# 我方坦克发射的子弹数量
Mytank_bullet_count = 2
# 我方坦克的生命次数
Mytank1_live_count = 2
Mytank2_live_count = 2
# 我方坦克初始位置
# Mytank_rect = (200, Window_height)
Font_size = 18
# 敌方坦克的步数
EnemyTank_step = 50
# 每次生成敌方坦克的数量
EnemyTank_count = 5
# 最大同时出现的坦克数量
EnemyTank_MaxCount = 15
# 敌方坦克的最大速度
EnemyTank_speed = 3
# 图片缩放比例
Rate = 1.5

# 第一次创建敌方坦克
Is_FirstCreateTank = True

# 游戏主逻辑类
class MainGame():
    # 游戏主窗口
    window = None
    # 类属性，用类名访问
    SCREEN_WIDTH = Window_width
    SCREEN_HEIGHT = Window_height
    # 创建我方坦克
    TANK_P1 = None
    TANK_P2 = None
    MyTnak_list = []
    # 创建我方大本营
    Myhome = Home.Home()
    # 统计敌方坦克总共生成多少数量
    Count = 0
    Is_gameover = False
    # 存储我方坦克子弹列表
    Bullet_list = []
    # 存储敌方坦克子弹列表
    EnemyBullet_list = []
    # 存储所有敌方坦克
    EnemyTank_list = []
    # 爆炸效果类列表
    Explode_list = []
    # 墙壁列表
    Wall_list = []
    # 食物列表
    Food_list = []
    # 子弹速度加速的倍数
    addCount = 1

    def __init__(self):
        pygame.init()
        # 自定义事件
        # 	-生成敌方坦克事件
        self.genEnemyEvent = pygame.USEREVENT + 1
        # 定制触发事件，每10s产生敌方坦克
        pygame.time.set_timer(self.genEnemyEvent, 10000)
        self.genfoodEvent = pygame.USEREVENT + 2
        # 定制触发事件，每30s产生敌方坦克
        pygame.time.set_timer(self.genfoodEvent, 30000)
        self.player = 0
    def clear(self):
        # 游戏主窗口
        MainGame.window = None
        # 创建我方坦克
        MainGame.TANK_P1 = None
        MainGame.MyTnak_list = []
        # 创建我方大本营
        MainGame.Myhome = Home.Home()
        # 统计敌方坦克总共生成多少数量
        MainGame.Count = 0
        MainGame.Is_gameover = False
        # 存储我方坦克子弹列表
        MainGame.Bullet_list = []
        # 存储敌方坦克子弹列表
        MainGame.EnemyBullet_list = []
        # 存储所有敌方坦克
        MainGame.EnemyTank_list = []
        # 爆炸效果类列表
        MainGame.Explode_list = []
        # 墙壁列表
        MainGame.Wall_list = []
        # 食物列表
        MainGame.Food_list = []
        # 子弹速度加速的倍数
        MainGame.addCount = 1
        global Mytank_speed, addTankSpped, Bullet_speed, addBulletSpeed, Mytank_bullet_count, Mytank1_live_count
        # 我方坦克速度
        Mytank_speed = 3
        addTankSpped = 1
        # 子弹速度
        Bullet_speed = 3
        # 子弹每次加速的速度
        addBulletSpeed = 1
        # 我方坦克发射的子弹数量
        Mytank_bullet_count = 2
        # 我方坦克的生命次数
        Mytank1_live_count = 2

    # 连续关卡,默认从第一关开始
    def main(self, stage=1):
        while True:
            # 先清空
            self.clear()
            # 每次玩完游戏后会返回一个关卡数
            stage = self.startGame(stage)

    # 开始游戏方法
    def startGame(self, stage):
        print(f"***********这是关卡{stage}************")
        _display.init()
        # 创建窗口，加载窗口,返回一个surface对象
        MainGame.window = _display.set_mode([MainGame.SCREEN_WIDTH, MainGame.SCREEN_HEIGHT])
        # 游戏选择开始画面
        self.player = self.show_start_interface()
        # 开始的时候，不产生食物，增加难度
        # self.createFood()
        _display.set_caption("坦克大战")
        # 创建我方坦克
        self.createMyTank(1)
        if self.player == 2:
            self.createMyTank(2)
        # 创建敌方坦克
        self.createEnemyTank()
        # 创建墙壁，选择关卡
        self.createbricks(stage)
        # 背景图
        bg_img = pygame.image.load("image/others/background.png")
        # 让窗口持续刷新操作,进入游戏主逻辑
        while True:
            # 给窗口完成一个填充颜色
            MainGame.window.fill(COLOR_BLACK)
            MainGame.window.blit(bg_img, (0, 0))
            # 在循环中持续完成事件的获取，处理事件
            self.getEvent()
            # 将绘制文字的小画布粘到窗口中
            # 将图像绘制到另一个图像上
            MainGame.window.blit(self.getTextSurface(f"剩余敌方坦克: {len(MainGame.EnemyTank_list)} 辆"), (0, 0))
            for tank in MainGame.MyTnak_list:
                if tank.id == 1:
                    MainGame.window.blit(self.getTextSurface(f"我方1号坦克的生命次数: {Mytank1_live_count} "), (420, 0))
                elif tank.id == 2:
                    MainGame.window.blit(self.getTextSurface(f"我方2号坦克的生命次数: {Mytank2_live_count} "), (420, 20))

            # 展示我方坦克
            self.blitMytank()
            # 展示敌方坦克,并且移动，发射子弹
            self.blitEnemyTank()
            # 展示我方坦克子弹,并且移动
            self.biltBullet()
            # 展示敌方子弹，并且移动
            self.blitEnemyBullet()
            # 展示爆炸效果
            self.biltExplodes()
            # 展示食物
            self.biltFoods()
            # 展示墙壁
            self.biltBricks()
            # 以秒为单位，降低刷新速度，从而降低移动速度
            # 展示我方大本营
            self.blitHome()
            # 判断游戏是否结束，三种情况，
            # 失败：
            #       我方大本营被击中，
            #       1个玩家 我方坦克死亡两次游戏失败 2 个玩家都死亡
            # 通关：敌方坦克全部被消灭且所有砖块消灭通关
            # print("墙壁数量:", len(scene.Map.Map_list))
            if MainGame.Is_gameover or (len(scene.Map.Map_list) == 8 or len(MainGame.EnemyTank_list) == 0):
                break
            time.sleep(0.01)
            # 窗口的刷新
            _display.update()
        # 有多种原因，游戏结束，还需要判断
        Stage = self.isGameOver()
        return Stage
    # 加载游戏选择界面
    def show_start_interface(self):
        font_size = 30
        width = Window_width
        height = Window_height

        title = self.getTextSurface('TANK', font_size, (255, 0, 0))
        content1 = self.getTextSurface('1 PLAYER (按1)', font_size, (255, 0, 0))
        content2 = self.getTextSurface('2 PLAYER (按1)', font_size, (255, 0, 0))

        trect = title.get_rect()
        trect.midtop = (width / 2, height / 3)

        crect1 = content1.get_rect()
        crect1.midtop = (width / 2, height / 1.8)
        crect2 = content2.get_rect()
        crect2.midtop = (width / 2, height / 1.6)
        MainGame.window.blit(title, trect)
        MainGame.window.blit(content1, crect1)
        MainGame.window.blit(content2, crect2)
        # 用于更新窗口显示并将所有绘制的变化呈现出来
        pygame.display.update()
        while True:
            # 用于获取pygame中已经发生的事件列表。它会返回一个列表，其中包含所有已发生的事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return 1
                    if event.key == pygame.K_2:
                        return 2
    # 游戏结束画面
    def show_end_interface(self, is_win):
        bg_img = pygame.image.load("image/others/background.png")
        MainGame.window.blit(bg_img, (0, 0))
        width = Window_width
        height = Window_height
        font_size = width // 10
        # 再来一局
        # againEvent = pygame.USEREVENT + 3
        # nextEvent = pygame.USEREVENT + 4
        if is_win:
            content = self.getTextSurface('恭喜通关！', font_size, (255, 0, 0))
            rect = content.get_rect()
            rect.midtop = (width / 2 + 10, height / 2 - 30)
            MainGame.window.blit(content, rect)
            # music = Music('./image')
        else:
            fail_img = pygame.image.load("image/others/gameover.png")
            rect = fail_img.get_rect()
            rect.midtop = (width / 2, height / 2 - 30)
            MainGame.window.blit(fail_img, rect)

        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("游戏结束")
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if is_win and event.key == pygame.K_2:
                    # if event.key == pygame.K_1:
                        print("*****进入关卡2*****")
                        # 进入关卡2
                        return 2
                    if not is_win and event.key == pygame.K_1:
                    # if event.key == pygame.K_2:
                        print("*****再玩一局*****")
                        # self.play_again(1)
                        return 1
    def createFood(self):
        for i in range(3):
            top = random.randint(1, 5)
            left = random.randint(1, 5)
            food = Food(i, top*100, left*100)
            MainGame.Food_list.append(food)
    # 我方坦克死亡后重生
    def createMyTank(self, id):
        myTank = Tank(player=id)
        myTank.rect.top = Window_height - myTank.rect.height
        myTank.oldTop = myTank.rect.top
        if id == 1:
            print("-----产生第一辆我方坦克-----")
            myTank.rect.left = 230
            myTank.oldLeft = 230
            MainGame.TANK_P1 = myTank
        elif id == 2:
            print("-----产生第二辆我方坦克-----")
            myTank.rect.left = 530
            myTank.oldLeft = 530
            MainGame.TANK_P2 = myTank
        MainGame.MyTnak_list.append(myTank)
        # 创建音乐对象
        music = Music('./image/start.wav')
        # 调用音乐方法
        music.play()

    # 创建敌方坦克
    def createEnemyTank(self):
        global Is_FirstCreateTank, EnemyTank_speed, EnemyTank_MaxCount, EnemyTank_count
        print(Is_FirstCreateTank)
        top = 0
        # 当前屏幕中，坦克的数量达到最大值，依次产生5辆，原来有11辆，在加5辆就16辆了，不能放在最开始
        if Is_FirstCreateTank:
            for i in range(EnemyTank_count):
                if len(MainGame.EnemyTank_list) >= EnemyTank_MaxCount:
                    return
                # 每个坦克的速度和位置都随机
                speed = random.randint(1, EnemyTank_speed)
                eTank = EnemyTank(i * 100, top, speed)
                # 给坦克编号,从1开始
                eTank.identify = MainGame.Count + 1
                MainGame.Count += 1
                # 出生时不能相撞
                MainGame.EnemyTank_list.append(eTank)
                print("*****生成敌方坦克*****")
            Is_FirstCreateTank = False
        else:
            for i in range(EnemyTank_count):
                print(EnemyTank_count)
                if len(MainGame.EnemyTank_list) >= EnemyTank_MaxCount:
                    return
                # 每个坦克的速度和位置都随机
                speed = random.randint(1, EnemyTank_speed)
                print(speed)
                eTank = EnemyTank(i * 100, top, speed)
                # 出生时不能相撞
                flag = 0
                for tank in MainGame.EnemyTank_list:
                    if pygame.sprite.collide_rect(tank, eTank):
                        # 不加入列表
                        flag = 1
                        break
                for tank in MainGame.MyTnak_list:
                    if pygame.sprite.collide_rect(tank, eTank):
                        # 不加入列表
                        flag = 1
                        break
                    # 这个逻辑差点写错了，不是写在for训话里面，要不让有一辆坦克没碰撞，就加一次
                if flag == 0:
                    eTank.identify = MainGame.Count + 1
                    MainGame.Count += 1
                    MainGame.EnemyTank_list.append(eTank)
                    print("*****生成敌方坦克******")

    # 创建墙壁,选择关卡
    def createbricks(self, stage=1):
        # 创建地图对象
        scenes = scene.Map()
        if stage == 1:
            print("----这是关卡1-----")
            scenes.create_stage1()
        elif stage == 2:
            print("----这是关卡2-----")
            scenes.create_stage2()
        # scenes.protect_home()

    def blitHome(self):
        MainGame.window.blit(MainGame.Myhome.image, MainGame.Myhome.rect)

    # 将敌方坦卡加入到窗口中，移动，射击
    def blitEnemyTank(self):
        # if len(MainGame.EnemyTank_list) == 0:
        #     MainGame.Is_gameover = True
        #     return
        for eTank in MainGame.EnemyTank_list:
            if not eTank.live:
                MainGame.EnemyTank_list.remove(eTank)
                continue
            eTank.displayEnemyTank()
            # 移动敌方坦克,随机切换方向
            eTank.randMove()
            # print("敌方坦克的速度 ", eTank.speed)
            # 进行撞墙检测,可以再move里面调用，也可以再后面
            eTank.tank_hit_wall()
            # 敌方坦克与食物的碰撞检测
            eTank.tank_hit_food()
            eTank.tank_hit_myTank()
            # 当前子弹数量不够时才能产生子弹， 每辆坦克只能发射3颗子弹, 0, 1, 2，发射完后如何再发射
            if eTank.bulletCount < 3:
                # print(eTank.bulletCount)
                ebullte = eTank.shot()
                # 与home的碰撞检测
                eTank.tank_hit_home()
                # 将子弹存储到敌方子弹列表，子弹不为空才存进去
                if ebullte:
                    # 将每颗子弹和发射它的坦克联系起来
                    ebullte.belong = eTank.identify
                    # 该坦克发射的子弹数加一，在子弹消失时，还要判断是哪个坦克发射的，进行减1
                    eTank.bulletCount += 1
                    MainGame.EnemyBullet_list.append(ebullte)
    def blitMytank(self):
        # 如果我方坦克存在，将我方坦克加到窗口中
        for myTank in MainGame.MyTnak_list:
            if myTank and myTank.live:
                myTank.displayTank()
                # 坦克持续移动，根据坦克的移动开关，没有停止就移动
                if not myTank.stop:
                    # print("这行代码在运行")
                    myTank.move()
                    # 进行撞墙检测，如果碰撞后，立刻回到上一次的位置，这里也可以写到move函数里面
                    myTank.tank_hit_wall()
                    # 与home的碰撞检测
                    myTank.tank_hit_home()
                    # 与食物的碰撞检测
                    myTank.tank_hit_food()
                    # 与敌方坦克相撞
                    myTank.tank_hit_enemyTank()
                    # 与另一辆坦克碰撞检测
                    myTank.tank_hit_otherTank()
            # 我方坦克不存在
            else:
                # 先删掉该坦克
                MainGame.MyTnak_list.remove(myTank)
                if self.player == 1:
                    if Mytank1_live_count > 0:
                        self.createMyTank(1)
                    else:
                        MainGame.Is_gameover = True
                if self.player == 2:
                    # 一辆死亡，一辆活着
                    # 1号坦克生命次数
                    if myTank.id == 1 and Mytank1_live_count > 0:
                        # print("-----------------------------------------------------")
                        self.createMyTank(1)
                    elif myTank.id == 2 and Mytank2_live_count > 0:
                        self.createMyTank(2)
                    # 一号坦克生命次数用完，还要2号
                    # 坦克生命次数为0
                        # 还没从列表中移除坦克，应该还有一辆
                    if len(MainGame.MyTnak_list) == 0:
                        MainGame.Is_gameover = True

    # 将墙壁加载到窗口
    def biltBricks(self):
        # if len(scene.Map.Map_list) == 8:
        #     MainGame.Is_gameover == True
        for brick in scene.Map.Map_list:
            if not brick.live:
                scene.Map.Map_list.remove(brick)
            MainGame.window.blit(brick.image, brick.rect)
    def biltFoods(self):
        for food in MainGame.Food_list:
            if not food.live:
                MainGame.Food_list.remove(food)
            food.displayfood()
    # 将我方坦卡发射的子弹和敌方坦克的子弹都加载到窗口中
    def biltBullet(self):
        for bullet in MainGame.Bullet_list:
            # 调用坦克自己的展示方法
            # 子弹不存在，从子弹列表中移除该子弹，不显示该子弹，也就不会打印子弹消失
            if not bullet.live:
                MainGame.Bullet_list.remove(bullet)
                continue
            # 子弹展示
            bullet.displayBullet()
            # 子弹显示
            bullet.move()
            # 我方子弹和敌方坦克碰撞检测
            bullet.hitEnemyTank()
            # 我方子弹和墙壁的碰撞检测
            bullet.hitWalls()
            # 我方子弹和我方大本营的碰撞检测
            bullet.hitMyHome()
            bullet.hitFood()
    # 展示敌方坦克的子弹
    def blitEnemyBullet(self):
        for bullet in MainGame.EnemyBullet_list:
            # 有子弹才显示，也可以在加入敌方子弹列表的时候就不加进来
            if not bullet.live:
                MainGame.EnemyBullet_list.remove(bullet)
                continue
            bullet.displayBullet()
            bullet.move()
            # 只有我方坦克存在且活着，才能检测，敌方子弹和我方坦克碰撞检测
            # for mytank in MainGame.MyTnak_list:
            #     if mytank and mytank.live:
            # 两个坦克都要检测
            bullet.hitMyTank()
            # 敌方子弹和墙壁的碰撞检测
            bullet.hitWalls()
            # 敌方子弹和我方大本营的碰撞检测
            bullet.hitMyHome()
            # 敌方子弹和食物的碰撞检测
            bullet.hitFood()


    # 展示爆炸效果
    def biltExplodes(self):
        for explod in MainGame.Explode_list:
            if explod.live:
                explod.displayExplode()
                music = Music('./image/blast.wav')
                music.play(3)
            else:
                MainGame.Explode_list.remove(explod)

    def isGameOver(self):
        stage = 1
        # if self.player == 2 and not MainGame.Myhome.live or (Mytank1_live_count == 0 and Mytank2_live_count ==0):
        #     print("-------------游戏失败1----------")
        #     MainGame.Myhome.set_dead()
        #     stage = self.show_end_interface(False)
        # elif self.player == 1 and (not MainGame.Myhome.live or Mytank1_live_count == 0):
        #     print("-------------游戏失败2----------")
        #     MainGame.Myhome.set_dead()
        #     stage = self.show_end_interface(False)
            # 降低游戏难度
        if len(scene.Map.Map_list) == 8 or len(MainGame.EnemyTank_list) == 0:
            # 敌方坦克被消灭
            print("-----------游戏通关------------- ")
            stage = self.show_end_interface(True)
        else:
            print("-------------游戏失败2----------")
            MainGame.Myhome.set_dead()
            stage = self.show_end_interface(False)
        # 前两条逻辑都没中
        return stage

    # 获取程序期间所有事件：（鼠标事件，键盘事件）
    def getEvent(self):
        pass
        # 1.获取所有事件,返回一个事件列表
        eventList = pygame.event.get()
        # 2.对事件进行判断处理
        # （1） 点击关闭按钮
        # （2）按下键盘的某个按键
        for event in eventList:
            # 判断event.type是否为QUIT，如果是的话，就退出程序
            if event.type == pygame.QUIT:
                exit()
                # 同一个类里调用其他函数用self
                # self.endGame()
            # 判断自定义事件
            if event.type ==self.genEnemyEvent:
                print("-----------------发生一次自定义事件-------------")
                self.createEnemyTank()
            if event.type == self.genfoodEvent:
                self.createFood()
            # 判断事件类型是否为按键按下，如果是，继续判断按键是哪一个按键，以此进行对应的处理
            if event.type == pygame.KEYDOWN:
                # 敌方坦克全部死亡后才能重生， 按5键
                if event.key == pygame.K_5 and len(MainGame.EnemyTank_list) == 0:
                    self.createEnemyTank()
                # 按esc键，坦克复活
                if event.key == pygame.K_ESCAPE:
                    if not MainGame.TANK_P1 or not MainGame.TANK_P1.live:
                        self.createMyTank(1)
                        # 坦克的live属性也要改变

                # 坦克不存在，不进行坦克的事件检测
                if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                    # 如果为键盘左键
                    if event.key == pygame.K_LEFT:
                        MainGame.TANK_P1.direction = 'L'
                        MainGame.TANK_P1.stop = False
                        # MainGame.TANK_P1.move()
                        print("坦克1向左调头，移动")
                    if event.key == pygame.K_RIGHT:
                        MainGame.TANK_P1.direction = 'R'
                        MainGame.TANK_P1.stop = False
                        # MainGame.TANK_P1.move()
                        print("坦克1向右调头，移动")
                    if event.key == pygame.K_UP:
                        MainGame.TANK_P1.direction = 'U'
                        MainGame.TANK_P1.stop = False
                        # MainGame.TANK_P1.move()
                        print("坦克1向上调头，移动")
                    if event.key == pygame.K_DOWN:
                        MainGame.TANK_P1.direction = 'D'
                        MainGame.TANK_P1.stop = False
                        # MainGame.TANK_P1.move()
                        print("坦克1向下调头，移动")
                    # 按下空格键， 我方坦克发射子弹
                    if event.key == pygame.K_SPACE:
                        # 限制，整个屏幕中只能存在3个子弹,没有等于号，当子弹数量等于3颗时，不在产生子弹
                        if len(MainGame.Bullet_list) < Mytank_bullet_count:
                            # 产生一颗子弹
                            bullet = MainGame.TANK_P1.shot()
                            # 吃到一次加速食物，子弹加速
                            bullet.speed += addBulletSpeed*MainGame.addCount
                            bullet.belong = 0
                            # 添加发射音效
                            music = Music('./image/fire.wav')
                            music.play()
                            MainGame.Bullet_list.append(bullet)
                            print("1发射子弹")
                        else:
                            print('子弹数量不足')
                        print(f'当前屏幕中的子弹数量{len(MainGame.Bullet_list)}')
                # 坦克2不存在，不进行坦克的事件检测
                if MainGame.TANK_P2 and MainGame.TANK_P2.live:
                    # 如果为键盘左键
                    if event.key == pygame.K_a:
                        MainGame.TANK_P2.direction = 'L'
                        MainGame.TANK_P2.stop = False
                        # MainGame.TANK_P1.move()
                        print("坦克2向左调头，移动")
                    if event.key == pygame.K_d:
                        MainGame.TANK_P2.direction = 'R'
                        MainGame.TANK_P2.stop = False
                        # MainGame.TANK_P1.move()
                        print("坦克2向右调头，移动")
                    if event.key == pygame.K_w:
                        MainGame.TANK_P2.direction = 'U'
                        MainGame.TANK_P2.stop = False
                        # MainGame.TANK_P1.move()
                        print("坦克2向上调头，移动")
                    if event.key == pygame.K_s:
                        MainGame.TANK_P2.direction = 'D'
                        MainGame.TANK_P2.stop = False
                        # MainGame.TANK_P1.move()
                        print("坦克2向下调头，移动")
                    # 按下空格键， 我方坦克发射子弹
                    if event.key == pygame.K_q:
                        # 限制，整个屏幕中只能存在3个子弹,没有等于号，当子弹数量等于3颗时，不在产生子弹
                        if len(MainGame.Bullet_list) < Mytank_bullet_count:
                            # 产生一颗子弹
                            bullet = MainGame.TANK_P2.shot()
                            # 吃到一次加速食物，子弹加速
                            bullet.speed += addBulletSpeed * MainGame.addCount
                            bullet.belong = 0
                            # 添加发射音效
                            music = Music('./image/fire.wav')
                            music.play()
                            MainGame.Bullet_list.append(bullet)
                            print("2发射子弹")
                        else:
                            print('子弹数量不足')
                        print(f'当前屏幕中的子弹数量{len(MainGame.Bullet_list)}')
            if event.type == pygame.KEYUP:
                # 坦克不存在，不进行坦克的事件检测
                if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                    # 如果松开的是方向键，才更改移动开关
                    if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                        MainGame.TANK_P1.stop = True
                if MainGame.TANK_P2 and MainGame.TANK_P2.live:
                    # 如果松开的是方向键，才更改移动开关
                    if event.key in (pygame.K_a, pygame.K_w, pygame.K_s, pygame.K_d):
                        MainGame.TANK_P2.stop = True

    # 绘画文字
    def getTextSurface(self, text, font_size=Font_size, color=COLOR_WHITE):
        # 字体初始化
        pygame.font.init()
        # 选中合适的字体
        font = pygame.font.SysFont('华文仿宋', font_size)
        textSurface = font.render(text, True, color)
        return textSurface
# 继承精灵类，实现碰撞检测
class BaseItem(pygame.sprite.Sprite):
    def __init__(self):
        # 初始化精灵类
        super().__init__()
        # pygame.sprite.Sprite.__init__()
class Tank(BaseItem):
    # 指定坦克图片，方向，位置区域
    def __init__(self, left=0, top=Window_height-20, player=1):
        super().__init__()
        if player == 1:
            # 四张图片分别代表四个方向的坦克
            image_u = pygame.image.load('./image/p1tankU.gif')
            image_u = pygame.transform.scale(image_u, (image_u.get_height() // 2, image_u.get_width() // 2))
            image_d = pygame.image.load('./image/p1tankD.gif')
            image_d = pygame.transform.scale(image_d, (image_d.get_height() // 2, image_d.get_width() // 2))
            image_l = pygame.image.load('./image/p1tankL.gif')
            image_l = pygame.transform.scale(image_l, (image_l.get_height() // 2, image_l.get_width() // 2))
            image_r = pygame.image.load('./image/p1tankR.gif')
            image_r = pygame.transform.scale(image_r, (image_r.get_height() // 2, image_r.get_width() // 2))
        elif player == 2:
            # 四张图片分别代表四个方向的坦克
            image_u = pygame.image.load('./image/p2tankU.gif')
            image_u = pygame.transform.scale(image_u, (image_u.get_height() // 2, image_u.get_width() // 2))
            image_d = pygame.image.load('./image/p2tankD.gif')
            image_d = pygame.transform.scale(image_d, (image_d.get_height() // 2, image_d.get_width() // 2))
            image_l = pygame.image.load('./image/p2tankL.gif')
            image_l = pygame.transform.scale(image_l, (image_l.get_height() // 2, image_l.get_width() // 2))
            image_r = pygame.image.load('./image/p2tankR.gif')
            image_r = pygame.transform.scale(image_r, (image_r.get_height() // 2, image_r.get_width() // 2))
        self.images = {
            # 加载后得到的也是一个surface对象
            'U': image_u,
            'D': image_d,
            'L': image_l,
            'R': image_r
        }
        # 坦克的初始方向
        self.direction = 'U'
        # 取出当前坦克的图片
        self.image = self.images[self.direction]
        # 坦克所在的区域,rect类有四个成员变量(left,top,width,height)
        self.rect = self.image.get_rect()
        # 指定坦克的初始化位置
        self.rect.left = left
        self.rect.top = top
        # 指定坦克的速度
        self.speed = Mytank_speed
        # 新增属性：坦克移动的开关
        self.stop = True
        # 是否存在
        self.live = True
        # 记录坦克移动之前的坐标,这里有bug
        # self.oldLeft = Window_width -200
        self.oldLeft = 0
        # self.oldTop = Window_height- 50
        self.oldTop = 0
        # 我方坦克编号
        self.id = player

    # 坦克的移动方法
    def move(self):
        if self.stop:
            return
        # 先记录上一次的位置
        # print(self.id, self.oldLeft, self.oldTop)
        self.oldTop, self.oldLeft = self.rect.top, self.rect.left
        if self.direction == 'L' and self.rect.left > 0:
            self.rect.left -= self.speed
        elif self.direction == 'R' and self.rect.left + self.rect.width < MainGame.SCREEN_WIDTH:
            self.rect.left += self.speed
        elif self.direction == 'U' and self.rect.top > 0:
            self.rect.top -= self.speed
        elif self.direction == 'D' and self.rect.top + self.rect.height < MainGame.SCREEN_HEIGHT:
            self.rect.top += self.speed
        # 移动完之后进行碰撞检测，碰撞还原而不是显示,如果在之前检测，则碰撞了不移动显示，下次还原，下一有碰撞了，就会抖动，
        # 所以碰撞了不应该直接显示，而是还原后才能显示
        # self.tank_hit_wall()

    # 坦克碰撞墙壁之后还原
    def stay(self):
        self.rect.top, self.rect.left = self.oldTop, self.oldLeft

    # 我方坦克和敌方坦克与墙壁的碰撞检测,碰撞到了还原位置
    def tank_hit_wall(self):
        for brick in scene.Map.Map_list:
            if pygame.sprite.collide_rect(self, brick):
                # print("*****坦克撞墙")
                self.stay()

    # 坦克与大本营的碰撞
    def tank_hit_home(self):
        if pygame.sprite.collide_rect(self, MainGame.Myhome):
            self.stay()
    def tank_hit_food(self):
        global Mytank_speed, Mytank1_live_count, Mytank_bullet_count,Is_add_MyBulletSpeed, addTankSpped
        for food in MainGame.Food_list:
            if pygame.sprite.collide_rect(self, food):
                print("吃到食物")
                food.live = False
                # 提高子弹的数量和速度，在事件里加的
                if food.kind == 0:
                    Mytank_bullet_count += 1
                    MainGame.addCount += 1
                # 提高坦克的速度
                elif food.kind == 1:
                    # 下一次速度不增加
                    # Mytank_speed += addTankSpped
                    self.speed += addTankSpped
                # 增加坦克的生命次数
                elif food.kind == 2:
                    Mytank1_live_count += 1
    # 与敌方坦克相撞
    def tank_hit_enemyTank(self):
        for eTank in MainGame.EnemyTank_list:
            if pygame.sprite.collide_rect(self, eTank):
                self.stay()
                eTank.stay()
    # 与另一辆坦克相撞
    def tank_hit_otherTank(self):
        for tank in MainGame.MyTnak_list:
            if self.id != tank.id and pygame.sprite.collide_rect(self, tank):
                print("---------我方两辆坦克相撞--------")
                self.stay()
                tank.stay()
    # 射击方法，返回一个子弹
    def shot(self):
        # 创建一个子弹
        return Bullet(self)

    # 展示坦克到窗口中
    def displayTank(self):
        # 重新设置坦克的图片
        self.image = self.images[self.direction]
        # 将坦克加入到窗口中
        MainGame.window.blit(self.image, self.rect)
# 敌方坦克
class EnemyTank(Tank):
    def __init__(self, left, top, speed=1):
        super().__init__(left, top)
        # 必选先调用父类的初始化方法，才能调用父类的属性
        # 图片集
        # 四张图片分别代表四个方向的坦克
        image_u = pygame.image.load('./image/enemy1U.gif')
        image_u = pygame.transform.scale(image_u, (image_u.get_height() // 2, image_u.get_width() // 2))
        image_d = pygame.image.load('./image/enemy1D.gif')
        image_d = pygame.transform.scale(image_d, (image_d.get_height() // 2, image_d.get_width() // 2))
        image_l = pygame.image.load('./image/enemy1L.gif')
        image_l = pygame.transform.scale(image_l, (image_l.get_height() // 2, image_l.get_width() // 2))
        image_r = pygame.image.load('./image/enemy1R.gif')
        image_r = pygame.transform.scale(image_r, (image_r.get_height() // 2, image_r.get_width() // 2))
        self.images = {
            # 加载后得到的也是一个surface对象
            'U': image_u,
            'D': image_d,
            'L': image_l,
            'R': image_r
        }
        # 坦克的初始方向为随机方向
        self.direction = self.randDirection()
        # 根据当前的方向，取出当前坦克的图片
        self.image = self.images[self.direction]
        # 坦克所在的区域,rect类有四个成员变量(left,top,width,height)
        self.rect = self.image.get_rect()
        # 指定坦克的初始化位置
        self.rect.left = left
        self.rect.top = top
        # 指定坦克的速度
        self.speed = speed
        # 坦克移动的开关
        self.stop = False
        # 步数,控制敌方坦克在某一方向移动的距离
        self.step = EnemyTank_step
        self.live = True
        # 记录每个敌方坦克当前在屏幕发射的子弹个数
        self.bulletCount = 0
        # 每辆坦克的标志
        self.identify = 0

    # 产生随机初始方向，放回一个随机方向
    def randDirection(self):
        # 包括0，和3
        num = random.randint(0, 3)
        directions = ['U', 'R', 'D', 'L']
        return directions[num]

    # 展示敌方坦克
    def displayEnemyTank(self):
        # # 重新设置坦克的图片
        # self.image = self.images[self.direction]
        # # 将坦克加入到窗口中
        # MainGame.window.blit(self.image, self.rect)
        # 调用父类的方法
        super().displayTank()

    # 敌方坦克移动
    def randMove(self):
        # 在某一个方向移动一定距离之后，随机更改移动方向
        if self.step == 0:
            self.direction = self.randDirection()
            self.step = EnemyTank_step
        else:
            # 步数减一，向某一个方向移动100次的循环次数
            self.step -= 1
            # 调用父类的移动方法
            self.move()
            # 一开始即碰在一起
            self.etank_hit_etank()

    # 敌方坦克射击后，产生一个子弹
    def shot(self):
        # 降低产生子弹的概率
        num = random.randint(1, 1000)
        # 不等于1返回一个空子弹
        if num < 10:
            return Bullet(self)
    def tank_hit_food(self):
        for food in MainGame.Food_list:
            if pygame.sprite.collide_rect(self, food):
                food.live = False
    def tank_hit_myTank(self):
        for tank in MainGame.MyTnak_list:
            if pygame.sprite.collide_rect(self, tank):
                tank.stay()
                self.stay()
    def etank_hit_etank(self):
        for eTank in MainGame.EnemyTank_list:
            if eTank.identify == self.identify:
                continue
            if pygame.sprite.collide_rect(self, eTank):
                self.stay()
class Explode():
    def __init__(self, tank):
        print("爆炸位置", tank.rect)
        self.rect = tank.rect
        # 爆炸效果离坦克有一定距离
        self.rect.left -= 35
        self.rect.top -= 15
        self.index = 0
        image0 = pygame.image.load('./image/blast0.gif')
        image0 = pygame.transform.scale(image0, (image0.get_width() / Rate, image0.get_height() / Rate))
        image1 = pygame.image.load('./image/blast1.gif')
        image1 = pygame.transform.scale(image1, (image1.get_width() / Rate, image1.get_height() / Rate))
        image2 = pygame.image.load('./image/blast2.gif')
        image2 = pygame.transform.scale(image2, (image2.get_width() / Rate, image2.get_height() / Rate))
        image3 = pygame.image.load('./image/blast3.gif')
        image3 = pygame.transform.scale(image3, (image3.get_width() / Rate, image3.get_height() / Rate))
        image4 = pygame.image.load('./image/blast4.gif')
        image4 = pygame.transform.scale(image4, (image4.get_width() / Rate, image4.get_height() / Rate))
        image5 = pygame.image.load('./image/blast5.gif')
        image5 = pygame.transform.scale(image5, (image5.get_width() / Rate, image5.get_height() / Rate))
        self.images = [image0, image1, image2, image3, image4, image5]
        self.image = self.images[self.index]
        # 决定爆炸效果是否展示
        self.live = True

    # 展示爆炸效果
    def displayExplode(self):
        if self.index < len(self.images) - 1:
            self.image = self.images[self.index]
            MainGame.window.blit(self.image, self.rect)
            self.index += 1
        else:
            self.index = 0
            self.live = False
class Bullet(BaseItem):
    def __init__(self, tank):
        super().__init__()
        # 子弹的方向取决于发射子弹的坦克方向
        # 子弹的初始坐标，取决于发射子弹的坦克位置
        # 子弹图片，为surface类
        self.image = pygame.image.load("./image/enemymissile.gif")
        self.image = pygame.transform.scale(self.image, (self.image.get_width() / Rate, self.image.get_height() / Rate))
        # 子弹初始方向
        self.direction = tank.direction
        # 子弹的初始位置
        self.rect = self.image.get_rect()
        # 标记子弹是哪个坦克发射的，0是我方坦克，1, 2, 3, 4, 5, 6, ....是敌方坦克
        self.belong = 0
        if self.direction == 'U':
            self.rect.left = tank.rect.left + (tank.rect.width - self.rect.width) / 2
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == 'D':
            self.rect.left = tank.rect.left + (tank.rect.width - self.rect.width) / 2
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.direction == 'L':
            self.rect.left = tank.rect.left - self.rect.width
            self.rect.top = tank.rect.top + (tank.rect.height - self.rect.height) / 2
        elif self.direction == 'R':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + (tank.rect.height - self.rect.height) / 2
        # 子弹的速度
        self.speed = Bullet_speed
        # 用来记录子弹是否存在，打到墙壁或者打到坦克
        self.live = True

    def move(self):
        # 要看看是哪个坦克发射的子弹消失
        if self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                self.live = False
                for eTank in MainGame.EnemyTank_list:
                    if eTank.identify == self.belong:
                        eTank.bulletCount -= 1
                print("子弹消失")
        elif self.direction == 'R':
            if self.rect.left + self.rect.width < MainGame.SCREEN_WIDTH:
                self.rect.left += self.speed
            else:
                self.live = False
                for eTank in MainGame.EnemyTank_list:
                    if eTank.identify == self.belong:
                        eTank.bulletCount -= 1
                print("子弹消失")
        elif self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                self.live = False
                for eTank in MainGame.EnemyTank_list:
                    if eTank.identify == self.belong:
                        eTank.bulletCount -= 1
                print("子弹消失")

        elif self.direction == 'D':
            if self.rect.top + self.rect.height < MainGame.SCREEN_HEIGHT:
                self.rect.top += self.speed
            else:
                self.live = False
                for eTank in MainGame.EnemyTank_list:
                    if eTank.identify == self.belong:
                        eTank.bulletCount -= 1
                print("子弹消失")

    def displayBullet(self):
        MainGame.window.blit(self.image, self.rect)

    # 我方子弹和敌方坦克，碰撞检测
    def hitEnemyTank(self):
        # 遍历敌方坦克，遍历错了，遍历成了子弹
        for eTank in MainGame.EnemyTank_list:
            # 只能检测两个精灵对象
            if pygame.sprite.collide_rect(eTank, self):
                eTank.live = False
                self.live = False
                print("敌方坦克位置:", eTank.rect)
                # 产生一个爆炸效果
                explod = Explode(eTank)
                # 将爆炸效果加入到爆炸效果列表中
                MainGame.Explode_list.append(explod)

    # 敌方子弹和我方坦克，碰撞检测
    def hitMyTank(self):
        # 主逻辑里面已经遍历了
        global Mytank1_live_count, Mytank2_live_count
        for myTank in MainGame.MyTnak_list:
            if pygame.sprite.collide_rect(self, myTank):
                # 追踪那个坦克发射的，可以多发射一颗
                for eTank in MainGame.EnemyTank_list:
                    if self.belong == eTank.identify:
                        eTank.bulletCount -= 1
                myTank.live = False
                self.live = False
                if myTank.id == 1:
                    Mytank1_live_count -= 1
                elif myTank.id == 2:
                    Mytank2_live_count -= 1
                # 产生爆炸效果，并加到爆炸效果里
                # print("我方坦克位置：", MainGame.TANK_P1.rect)
                explode = Explode(myTank)
                MainGame.Explode_list.append(explode)

    # 子弹和墙壁的碰撞检测
    def hitWalls(self):
        for brick in scene.Map.Map_list:
            if pygame.sprite.collide_rect(self, brick):
                # 追踪那个坦克发射的，可以多发射一颗
                for eTank in MainGame.EnemyTank_list:
                    if self.belong == eTank.identify:
                        eTank.bulletCount -= 1
                self.live = False
                if brick.kind == 'Brick':
                    brick.live = False

    def hitMyHome(self):
        if pygame.sprite.collide_rect(self, MainGame.Myhome):
            for eTank in MainGame.EnemyTank_list:
                if self.belong == eTank.identify:
                    eTank.bulletCount -= 1
            print("子弹与home碰撞")
            MainGame.Myhome.live = False
            self.live = False
            MainGame.Is_gameover = True
            # 产生爆炸效果，并加到爆炸效果里
            # print("我方坦克位置：", MainGame.TANK_P1.rect)
            # explode = Explode(MainGame.TANK_P1)
            # MainGame.Explod_list.append(explode)
    def hitFood(self):
        for food in MainGame.Food_list:
            if pygame.sprite.collide_rect(self, food):
                for eTank in MainGame.EnemyTank_list:
                    if self.belong == eTank.identify:
                        eTank.bulletCount -= 1
                self.live = False
                food.live = False
class Music():
    def __init__(self, fileName):
        self.filename = fileName
        # 初始化
        pygame.mixer.init()
        pygame.mixer.music.load(self.filename)
    # 开始播放音乐
    def play(self, count=1):
        pygame.mixer.music.play(loops=count)
class Food(pygame.sprite.Sprite):
    def __init__(self, kind, left, top):
        pygame.sprite.Sprite.__init__(self)
        # 使得坦克子弹可碎钢板,提高子弹的射击速度,  # 坦克升级，提高坦克的移动速度,  # 坦克生命次数+1
        self.images = ['image/food/food_gun.png', 'image/food/food_star.png', 'image/food/food_tank.png']
        # 所有食物
        self.image = pygame.image.load(self.images[kind])
        self.kind = kind
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = left, top
        # 是否存在
        self.live = True

    def displayfood(self):
        MainGame.window.blit(self.image, self.rect)
if __name__ == '__main__':
    game = MainGame()
    game.main(1)
