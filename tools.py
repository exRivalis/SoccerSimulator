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

class MyState(object):
	
	def __init__(self,state,idteam,idplayer) :
		self.state = state
		self.key = (idteam, idplayer)
		
		self.my_position = self.state.player_state(self.key[0], self.key[1]).position
		self.ball_position = self.state.ball.position
		self.but_adv = Vector2D(150, 45) if self.key[0] == 1 else Vector2D(0, 45)	
		#recup joueur 
		self.all_players = self.state.players
		self.co_players = [p  for p in self.all_players if (p[0] == self.key[0] and p[1] != self.key[1])]
		self.adv_players = [p  for p in self.all_players if p[0] != self.key[0]]
		#can the player shoot in the ball
		self.can_shoot = True if self.my_position.distance(self.ball_position) < 0.82 else False
		
		#est proche de la balle
		self.near_ball = True if self.my_position.distance(self.ball_position) < 20 else False
	
	def aller(self, p) :
		return SoccerAction(p-self.my_position, Vector2D())
	
	def shoot(self, p) :
		return SoccerAction(Vector2D(), p-self.my_position)
		
	#recup adv le plus proche
	def adv_nearby(self):
		players = self.adv_players
		if len(players) == 0:
			return None
		pp = players[0]
		for p in players:
			#print self.my_position.distance(self.state.player_state(p[0], p[1]).position)
			#print self.my_position.distance(self.state.player_state(pp[0], pp[1]).position)
			if self.my_position.distance(self.state.player_state(p[0], p[1]).position) < self.my_position.distance(self.state.player_state(pp[0], pp[1]).position):
				pp = p
		return self.state.player_state(pp[0], pp[1])
	
	#true if player p near ball
	def p_near_ball(self, p):
		return True if self.ball_position.distance(self.state.player_state(p[0], p[1]).position) < 20 else False
				
		
## Strategie aleatoire
class RandomStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Random")
    def compute_strategy(self,state,id_team,id_player):
        return SoccerAction(Vector2D.create_random(-1,1),Vector2D.create_random(-1,1))

#creation strategy
class Attaquant(Strategy):
	def __init__(self, name="attaquant"):
		Strategy.__init__(self, name)
	def compute_strategy(self, state, idteam, idplayer):
		#on cree un objet qui sera notre joueur et sur lequel on agira
		mstate = MyState(state,idteam,idplayer)
		#return mstate.adv_nearby()
		return mstate.aller(mstate.ball_position) + mstate.shoot(mstate.but_adv)


class AttaquantPlus(Strategy):
	def __init__(self, name="attaquantPlus"):
		Strategy.__init__(self, name)
	def compute_strategy(self, state, idteam, idplayer):
		mstate = MyState(state, idteam, idplayer)
		
		for p in mstate.co_players:
	#if un autre joueur proche de la balle et la balle au dela de la moitie du terrainaller de lavant
			if  mstate.p_near_ball(p) and mstate.ball_position.distance(mstate.but_adv) < 50:
				print mstate.state.player_state(p[0], p[1]).name
				return Vector2D(1,0)
			elif mstate.can_shoot :
				return mstate.shoot(mstate.but_adv)
			
		#return mstate.aller(mstate.ball_position) + mstate.shoot(mstate.but_adv)

		
class Defenseur(Strategy):
	def __init__(self, name="defenseur"):
		Strategy.__init__(self, name)
	def compute_strategy(self, state, idteam, idplayer):
		mstate = MyState(state,idteam,idplayer)
	
		#si defenseur plus proche de la ball que de l'adv va vers la balle et tir dedans sinon va vers l'adv
		if mstate.my_position.distance(mstate.ball_position) < mstate.my_position.distance(mstate.adv_nearby().position):
			return mstate.aller(mstate.ball_position) + mstate.shoot(mstate.but_adv)

		#
		return mstate.aller(mstate.adv_nearby().position - Vector2D(0,0))
		#return mstate.aller(mstate.ball_position()) + mstate.shoot(mstate.but_adv())
		
class DefenseurPlus(Strategy):
	def __init__(self, name="defenseurPlus"):
		Strategy.__init__(self, name)
	def compute_strategy(self, state, idteam, idplayer):
		mstate = MyState(state, idteam, idplayer)
		
		
		
		
		
		
		
		
		
