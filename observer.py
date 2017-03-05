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

class Observer(object):
	MAX_STEP = 80
	def __init__(self, simu):
		self.simu = simu
		self.simu.listeners += self #ajout de l'observer
		
	def begin_match(self, team1, team2, state):
		#init des parametres
		self.last, self.cpt, self.cpt_tot = 0, 0, 0
	
	def begin_round(self, team1, team2, state):
		ball = Vector2D(130, 40)
		#pour tir
		#self.simu.state.ball.position = Vector2D(120, 45) #placement de la balle au debut
		#self.simu.state.states[(1, 0)].position = ball - Vector2D(0.5, 0) #placement du joueur au debut
		
		#pour aller balle
		self.simu.state.ball.position = ball
		self.simu.state.states[(1, 0)].position = ball - Vector2D(70, 45)#position joueur 0
		self.simu.state.states[(1,1)].position = ball - Vector2D(10, 10)#position joueur qui a la balle
		#print self.simu.team1.strategies[0].compute_strategy(self.simu.state, 1, 0) 
		#self.simu.shoot = Vector2D(10, 0)
		self.last = self.simu.step
	
	def update_round(self, team1, team2, state):
			if self.simu.step > self.last + self.MAX_STEP: self.simu.end_round() 
			
	def end_round(self, team1, team2, state):
		if state.goal > 0: self.cpt += 1
		self.cpt_tot += 1
		self.res = self.cpt*1./self.cpt_tot
		if self.cpt_tot > 10:
			print self.res
			self.simu.end_match()
	"""		
	def end_round(self, team1, team2, state):
		if state.goal > 0: self.cpt += 1
		self.cpt_tot += 1
		self.res = self.cpt*1./self.cpt_tot
		if self.cpt_tot > 50:
			print self.res
			self.simu.end_match()
	"""	
	"""
			if self.simu.step == self.MAX_STEP:
			self.simu.end_match()
			"""
