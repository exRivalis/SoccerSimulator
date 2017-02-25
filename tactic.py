#toutes les tactiques utilisees par les strategies
#les objets de base
from soccersimulator import Vector2D, SoccerState, SoccerAction

#objets pour un match
from soccersimulator import Simulation, SoccerTeam, Player, show_simu, SoccerTournament

#importer la strategie de base
from soccersimulator import Strategy

#toutes les constantes
from soccersimulator import settings

#module math
import math

from tools import MyState

#tactiques pour 1vs1
class STactic(MyState):
	def __init__(self, state, idteam, idplayer):
		self.state = state
		self.idteam = idteam
		self.idplayer = idplayer
		
	
	@property
	def	defendre(self):
		ms = MyState(self.state, self.idteam, self.idplayer)
		
		adv = ms.adv_players[0]		#adv
		me = ms.my_position		#moi-meme
		
		sens = ms.sens 			#de quel cote je suis
		
		ball = ms.ball_position
		but_adv = ms.but_adv
		but = ms.but
		
		v_ball = ms.v_ball
		
		if ms.dist_ball < 2:
			return ms.passe(but_adv - me)
		#return ms.aller(ball + 3*sens*v_ball)
			return ms.aller_ball
		
	
	@property
	def attaquer(self):
		ms = MyState(self.state, self.idteam, self.idplayer)
		
		adv = ms.adv_players[0]		#adv
		me = ms.my_position		#moi-meme
		
		sens = ms.sens 			#de quel cote je suis
		
		ball = ms.ball_position
		but_adv = ms.but_adv
		but = ms.but
		
		v_ball = ms.v_ball
		
		if sens*v_ball.x < 0:	#la balle va dans ma direction
			if sens*me.x < sens*ball.x : 			#je suis derriere la balle
					return ms.aller_but_adv #+ ms.passe(but_adv)			#je vais marquer
		return ms.aller(ball) + ms.passe(but_adv)  #
			#return self.defendre		#aller derrier la balle si elle est derriere moi
	
	
	@property
	def goal(self):
		ms = MyState(self.state, self.idteam, self.idplayer)
		return ms.my_position
		
#tactiques pour 2vs2
class TTactic(object):
	def __init__(self, state, idteam, idplayer):
		self.state = state
		self.idteam = idteam
		self.idplayer = idplayer
		
		
	@property
	def goal(self):
		ms = MyState(self.state, self.idteam, self.idplayer)
		
		return ms.aller(ms.but)

	@property
	def	defendre(self):
		ms = MyState(self.state, self.idteam, self.idplayer)
		advs = ms.adv_players	#tous les adversaires
		coes = ms.co_players	#tous les coequipiers
		
		adv = ms.adv_nearby		#adv le plus proche
		coeq = ms.coeq_nearby	#mon coeq le plus proche
		me = ms.my_position		#moi-meme
		
		sens = ms.sens 			#de quel cote je suis
		
		ball = ms.ball_position
		but_adv = ms.but_adv
		but = ms.but
		
		v_ball = ms.v_ball
		v_coeq = ms.v_coeq
		
		if ms.dist_ball < 2:
			return ms.passe(coeq)
		return ms.aller(ball + 3*sens*v_ball)
		

	@property
	def attaquer(self):
		ms = MyState(self.state, self.idteam, self.idplayer)
		#sens = 1 if self.idteam == 1 else -1 #si je suis a gauche 1 sinon je suis a droite -1
		
		advs = ms.adv_players	#tous les adversaires
		coes = ms.co_players	#tous les coequipiers
		
		adv = ms.adv_nearby		#adv le plus proche
		coeq = ms.coeq_nearby	#mon coeq le plus proche
		me = ms.my_position		#moi-meme
		
		v_coeq = ms.v_coeq
		
		sens = ms.sens 			#de quel cote je suis
		
		ball = ms.ball_position	#position balle
		v_ball = ms.v_ball		#vect vitesse de la balle
		but_adv = ms.but_adv	#position but adv
		but = ms.but
		
		cpt = 0
		for a in advs:
			for c in coes:
				if a.distance(but) < c.distance(but):
					cpt += 1
		in_my_zone = True if cpt == 2 else False
		
		if sens*v_ball.x < 0:	#la balle va dans ma direction
			if sens*me.x < sens*ball.x : 			#je suis derriere la balle
				if me.distance(but_adv) < coeq.distance(but_adv): #je suis plus proche des but que mon coeq
					return ms.aller_but_adv 			#je vais marquer
				return ms.aller(ball) + ms.passe(coeq)  #sinon je fais la passe
			return self.defendre		#aller derrier la balle si elle est derriere moi
		if me.distance(but_adv) < coeq.distance(but_adv):#je suis plus proche des buts adv que mon coeq
			if ms.dist_ball < coeq.distance(ball): #je suis plus proche de la balle aussi 
				return ms.aller(ball) + ms.passe(but_adv)
			return ms.aller(but_adv - sens*Vector2D(7, 0))			#je fonce
		return ms.aller(ball) + ms.passe(coeq) 	#je fonce sur la balle et je fais la passe
			
#tactiques pour 4vs4
class FTactic(MyState):
	def __init__(self, state, idteam, idplayer):
		self.state = state
		self.idteam = idteam
		self.idplayer = idplayer
		
	
	@property
	def	defendre(self):
		ms = MyState(self.state, self.idteam, self.idplayer)
		return ms.my_position
		
	
	@property
	def attaquer(self):
		ms = MyState(self.state, self.idteam, self.idplayer)
		return ms.my_position
	
	
	@property
	def goal(self):
		ms = MyState(self.state, self.idteam, self.idplayer)
		return ms.my_position
