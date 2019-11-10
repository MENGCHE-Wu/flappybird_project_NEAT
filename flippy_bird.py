import pygame
import neat
import time
import os
import random
pygame.font.init()
WIN_WIDTH = 600
WIN_HEIGHT= 800
GEN = 0
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))
STAT_FONT = pygame.font.SysFont("comicsans",50)
class Bird:
	IMGS = BIRD_IMGS
	MAX_ROTATION = 25
	ROT_VEL = 20
	ANIMATION_TIME= 5

	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.tilt = 0
		self.tick_count = 0
		self.vel = 0
		self.height = self.y
		self.img_count = 0
		self.img = self.IMGS[0]

	def jump(self):
		self.vel = -10.5
		self.tick_count = 0
		self.height = self.y
		

	def move(self): 
		self.tick_count += 1

		#d = self.vel*self.tick_count + 1.5*((self.tick_count)**2)
		d = self.vel*(self.tick_count) + 0.5*(3)*(self.tick_count)**2
		
		#self.vel += 3
		#print (d)
		if d >= 16:
			d= d / abs(d)*16
		if d < 0:
			d -= 2
		print(d,self.vel,self.tick_count)
		self.y = self.y + d

		if d < 0 or self.y < self.height +50:
			if self.tilt < self.MAX_ROTATION:
				self.tilt = self.MAX_ROTATION
		else:
			if self.tilt > -90:
				self.tilt -= self.ROT_VEL
		#if self.y <= 700:
		#	self.jump()
		if self.y <= -5:
			self.y = -5

	def draw(self,win):
		self.img_count +=1

		if self.img_count < self.ANIMATION_TIME:
			self.img = self.IMGS[0]
		elif self.img_count < self.ANIMATION_TIME*2:
			self.img = self.IMGS[1]
		elif self.img_count < self.ANIMATION_TIME*3:
			self.img = self.IMGS[2]	
		elif self.img_count < self.ANIMATION_TIME*4:
			self.img = self.IMGS[1]
		elif self.img_count == self.ANIMATION_TIME*4 +1:
			self.img = self.IMGS[0]
			self.img_count = 0
		if self.tilt <= -80:
			self.img = self.IMGS[1]
			self.img_count = self.ANIMATION_TIME*2


		rotated_image = pygame.transform.rotate(self.img,self.tilt)
		new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft =(self.x,self.y)).center)
		win.blit(rotated_image, new_rect.topleft)

	def get_mask(self):
		return pygame.mask.from_surface(self.img)


class Pipe:
	
	VEL = 5
	def __init__(self,x):
		self.gap = 200
		self.top = 0
		self.buttom = 0
		self.x = x
		self.PIPE_TOP = pygame.transform.flip(PIPE_IMG,False,True)
		self.PIPE_BOTTOM = PIPE_IMG
		self.scored = False
		self.passed = False 
		self.score = 0
		self.set_height()
	def set_height(self):
		self.height = random.randrange(50,550)
		self.top = self.height - self.PIPE_TOP.get_height()
		self.bottom = self.height + self.gap

	def move(self):
		if self.score >=5:
			for i in range(self.score//5):
				if self.VEL < 5+((self.score//5)+1):
					self.VEL += 1
		self.x -= self.VEL

	def draw(self,win):
		#print(self.x,self.top)
		win.blit(self.PIPE_TOP,(self.x,self.top))
		win.blit(self.PIPE_BOTTOM,(self.x,self.bottom))

	def collide(self,bird):
		birds_mask = bird.get_mask()
		top_mask = pygame.mask.from_surface(self.PIPE_TOP)
		bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

		top_offset = (self.x - bird.x , self.top - round(bird.y))
		bottom_offset = (self.x - bird.x , self.bottom - round(bird.y))

		b_point = birds_mask.overlap(bottom_mask , bottom_offset)
		t_point = birds_mask.overlap(top_mask , top_offset)
		if t_point or b_point:
			return True
		return False


class Base:
	VEL = 5
	WIDTH = BASE_IMG.get_width()
	IMG = BASE_IMG

	def __init__(self,y):
		self.y = y
		self.x1 = 0
		self.x2 = self.WIDTH

	def move(self):
		self.x1 -= self.VEL
		self.x2 -= self.VEL
		if self.x2 <= 0:
			self.x1 = self.x2+self.WIDTH

		if self.x1 <=0:
			self.x2 = self.x1 +self.WIDTH

	def draw(self,win):
		win.blit(self.IMG,(self.x1,self.y))
		win.blit(self.IMG,(self.x2,self.y))
		#print("x1,x2 = ",self.x1,self.x2)

class Bg():
	VEL = 0.5
	IMG = BG_IMG
	WIDTH = IMG.get_width()-5
	def __init__(self,y):
		self.y = y
		self.x1 = 0
		self.x2 = self.WIDTH
	def move(self):
		self.x1 -= self.VEL
		self.x2 -= self.VEL

		if self.x1+ self.WIDTH <= 0:
			self.x1 = self.x2 + self.WIDTH

		if self.x2+ self.WIDTH <=0:
			self.x2 = self.x1 + self.WIDTH

	def draw(self,win):
		win.blit(self.IMG,(self.x1,self.y))
		win.blit(self.IMG,(self.x2,self.y))











def draw_window(win,birds,pipes,base,bg,score,FPS,GEN):
	#win.blit(BG_IMG,(0,-30))
	bg.draw(win)
	bg.move()
	for bird in birds:
		bird.draw(win)
		
	for pipe in pipes:
		pipe.score = score
		pipe.draw(win)
		pipe.move()
	base.draw(win)
	base.move()
	text = STAT_FONT.render("Score: "+str(score),1,(0,0,0))
	fps = STAT_FONT.render(str(int(FPS)), True, (0,0,0))
	gen = STAT_FONT.render("GEN:"+str(int(GEN)), True, (0,0,0))
	win.blit(text,(WIN_WIDTH - 10 - text.get_width(),10 ))
	win.blit(fps,(0,0))
	win.blit(gen,(0,40))
	pygame.display.update()

def main(genomes,config):
	global GEN
	clock = pygame.time.Clock()
	nets =[]
	ge = []
	birds = []
	GEN +=1 

	for _,g in genomes:
		net = neat.nn.FeedForwardNetwork.create(g,config)
		nets.append(net)
		birds.append(Bird(230,350))
		g.fitness = 0
		ge.append(g)

	pipes = [Pipe(500)]
	base = Base(730)
	bg = Bg(-30)
	score = 0
	win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
	run = True
	while run:
		clock.tick(30)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				quit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				bird.jump()
		pipe_ind = 0
		if len(birds)>0:
			if len(pipes)>1 and pipes[0].passed:
				pipe_ind = 1
		else:
			run = False
			break
		for x,bird in enumerate(birds):
			bird.move()
			ge[x].fitness += 0.1

			#output = nets[x].activate((bird.y,abs(bird.y-pipes[pipe_ind].height),abs(bird.y - pipes[pipe_ind].bottom)))
			output = nets[birds.index(bird)].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
			if output[0] > 0.5:
				bird.jump()
		for x,bird in enumerate(birds):

			if pipes[0].collide(bird) or bird.y +bird.img.get_height() >= 730:
				ge[x].fitness -= 20
				
				nets.pop(birds.index(bird))
				ge.pop(birds.index(bird))
				birds.pop(birds.index(bird))

			if bird.x >= pipes[0].x+pipes[0].PIPE_TOP.get_width():
				pipes[0].passed = True
				if pipes[0].scored == False:
					pipes[0].scored = True
					score += 1
					for g in ge:
						g.fitness += 5

		if pipes[0].x <=200:
			if len(pipes)<2:
				pipes.append(Pipe(600))
		if pipes[0].x <= -1*pipes[0].PIPE_TOP.get_width():
			pipes.pop(0)
		FPS = clock.get_fps()
		draw_window(win,birds,pipes,base,bg,score,FPS,GEN)




def run(config_path):
	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction , 
					neat.DefaultSpeciesSet,neat.DefaultStagnation,
					config_path)
	p = neat.Population(config)

	p.add_reporter(neat.StdOutReporter(True))
	stats = neat.StatisticsReporter()
	p.add_reporter(stats)

	winner=p.run(main,50)

if __name__ == "__main__":
	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir,"config-feedforward.txt")
	run(config_path)