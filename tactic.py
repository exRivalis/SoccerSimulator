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
		return ms.my_position
		
	
	@property
	def attaquer(self):
		ms = MyState(self.state, self.idteam, self.idplayer)
		return ms.my_position
	
	
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
	def attaquer(self):
		ms = MyState(self.state, self.idteam, self.idplayer)
		#sens = 1 if idteam == 1 else -1 #si je suis a gauche 1 sinon je suis a droite -1
		
		advs = ms.adv_players	#tous les adversaires
		coes = ms.co_players	#tous les coequipiers
		
		#je suis plus proche de la balle
		if ms.my_position.distance(ms.ball_position) < ms.coeq_nearby.distance(ms.ball_position):
			#je suis plus proche des but
			if ms.coeq_nearby.distance(ms.but_adv) < (ms.my_position.distance(ms.but_adv) - 5):
				return ms.aller_ball + ms.aller_but_adv
			return ms.aller_ball + ms.passe(ms.coeq_nearby + ms.sens*Vector2D(5, 0)) 
		
		#a egale dist
		elif ms.my_position.distance(ms.ball_position) == ms.coeq_nearby.distance(ms.ball_position):
			#regarder le plus proche des but aussi
			if ms.my_position.distance(ms.but_adv) < ms.coeq_nearby.distance(ms.but_adv):
				return ms.aller_but_adv
			"""elif ms.my_position.distance(ms.but_adv) == ms.coeq_nearby.distance(ms.but_adv):
				if ms.key[1] == 0:#joueur1 vers les buts
					return ms.aller_but_adv
				return ms.aller_ball + ms.passe(ms.coeq_nearby)
			"""	
			return ms.aller_ball + ms.passe(ms.coeq_nearby)
			
		#si l'autreplus priche dela balle, aller but_adv
		return ms.aller_but_adv
		
	@property
	def goal(self):
		ms = MyState(self.state, self.idteam, self.idplayer)
		
		#si adv pres de moi
		if ms.my_position.distance(ms.adv_nearby) < 10:
			#aller ball + degager
			ms.aller_ball + ms.passe(ms.but_adv)
		
		#sinon si moi pres balle
		if ms.near_ball:
			return self.attaquer
			
		#adv pres mes but 
		if ms.adv_nearby.distance(ms.but) < 20:
			#aller pres mes buts
			ms.aller(ms.but + ms.sens*Vector2D(-7, 0))
		
		#sinon 
		return self.attaquer
	
	@property
	def	defendre(self):
		ms = MyState(self.state, self.idteam, self.idplayer)
		
		#si coeq a la balle et on loins de nos but attaquer
		if ms.co_near_ball and ms.my_position.distance(ms.but) > 30:
			return self.attaquer
		return self.attaquer
		"""
		#je suis a cote de la balle
		if ms.near_ball :
			#return ms.aller_ball + ms.aller_but_adv
			
			#si coeq vrmnt + proche des but que moi, passer la balle
			if ms.coeq_nearby.distance(ms.but_adv) < (ms.my_position.distance(ms.but_adv) - 5):
				return ms.passe(ms.coeq_nearby)
			#sinon aller vers but adv avec la balle et marquer des que possible
			else : 
				return ms.aller_ball + ms.aller_but_adv
			
		#je suis pas a cote balle mais mon coeq si
		elif ms.co_near_ball:
			return ms.aller_but_adv
			
			advs_haut = 0
			for a in advs:
				advs_haut += 1 if a.y < 45 else 0
			
			#si les deux advs en haut contourner par le bas
			if advs_haut ==  2:
				#si je suis + proche de la balle je vais vers la balle
				if (ms.my_position.distance(ms.ball_position) - 5) < ms.coeq_nearby.distance(ms.ball_position):
					return ms.aller_ball
				#sinon aller but_adv
				return ms.aller(ms.but_adv + ms.sens*Vector2D(-5, 0) + Vector2D(0, 10))	
			
			#sinon par le haut
			if (ms.my_position.distance(ms.ball_position)) < ms.coeq_nearby.distance(ms.ball_position):
				if ms.me_near_co and ms.key[1] == 0:
					return ms.aller_but_adv
				#elif ms.me_near_co:
				return ms.aller_ball + ms.passe(ms.coeq_nearby)
			#sinon aller but_adv
			return	ms.aller(ms.but_adv)# + ms.sens*Vector2D(-5, 0) + Vector2D(0,-10))	
			
		#si les deux loins de la balle j1 vers balle et j2 vers but_adv
		#si je suis plus proche des but, jy vais sinon je vais vers la balle
		if ms.my_position.distance(ms.but_adv) < ms.coeq_nearby.distance(ms.but_adv):
			return ms.aller_but_adv
		elif ms.my_position.distance(ms.but_adv) == ms.coeq_nearby.distance(ms.but_adv):
			if ms.key[1] == 0:
				return ms.aller_but_adv
			return ms.aller_ball# + ms.passe(ms.coeq_nearby)
		return ms.aller_ball #+ ms.passe(ms.but_adv) #ms.aller_but_adv
	"""

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
