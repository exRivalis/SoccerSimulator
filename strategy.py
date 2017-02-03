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
		
		#determination sens en fonction du num equipe
		adv = mstate.adv_nearby()
		sens = 1
		pos = 50
		if adv[0] == 2 :
			sens = 1
			pos = 100
		else:
			sens = -1
			pos = 50
		coeq = mstate.coeq_nearby()
		
		"""une variable qui va etudier cas : 1-si l'adversaire est plus proche de la balle que nous on retourne en defense
		sinon on a 2-notre jouer le + proche -> va a la balle et fait une action
		l'action passe s'il est en defense et tir vers les buts sinon
		et l'autre joueur avance vers la balle si l'autre joueur est en defense sinon va vers les buts'
		"""
		#return mstate.adv_nearby()
		if mstate.key[1] == 0:
			me = mstate.my_position.distance(mstate.ball_position)
			lautre = mstate.state.player_state(coeq[0], coeq[1]).position.distance(mstate.ball_position)
			if me < lautre:
				return mstate.aller(mstate.ball_position)	+ mstate.shoot(mstate.but_adv)
			
			if mstate.my_position.x*sens < pos*sens :
				return mstate.aller(mstate.my_position + sens*Vector2D(10, 0))
		#si adv + proche est a x > 50
		#mstate.state.player_state(adv[0], adv[1]).position.x*sens > sens*pos
		
		elif mstate.my_position.distance(mstate.state.player_state(coeq[0], coeq[1]).position) > 40:
			if mstate.can_shoot :
				return mstate.shoot(mstate.state.player_state(mstate.key[0], 0).position)
			return mstate.aller(mstate.ball_position)
		else :
			return mstate.aller(Vector2D(mstate.my_position.x, 45))

class AttaquantPlus(Strategy):
	def __init__(self, name="attaquantPlus"):
		Strategy.__init__(self, name)
	def compute_strategy(self, state, idteam, idplayer):
		mstate = MyState(state, idteam, idplayer)
		
		for p in mstate.co_players:
	#if un autre joueur proche de la balle et la balle au dela de la moitie du terrainaller de lavant
			if  mstate.p_near_ball(p) and mstate.ball_position.distance(mstate.but_adv) < 50:
				#print mstate.state.player_state(p[0], p[1]).name
				return mstate.aller(Vector2D(1,0))
			elif mstate.can_shoot :
				return mstate.shoot(mstate.but_adv)
			return mstate.aller(Vector2D(75, 45))
			
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
		return mstate.drible()
		
		
class Defenseur(Strategy):
	def __init__(self, name="defenseur"):
		Strategy.__init__(self, name)
	def compute_strategy(self, state, idteam, idplayer):
		mstate = MyState(state,idteam,idplayer)
	
		#si defenseur plus proche de la ball que de l'adv va vers la balle et tir dedans sinon va vers l'adv
		p = mstate.adv_nearby()
		if mstate.my_position.distance(mstate.ball_position) < mstate.my_position.distance(mstate.state.player_state(p[0], p[1]).position):
			p = mstate.coeq_nearby()
			return mstate.aller(mstate.ball_position) + mstate.shoot(mstate.state.player_state(p[0], p[1]).position)

		return mstate.aller(mstate.state.player_state(p[0], p[1]).position)
		#return mstate.aller(mstate.ball_position()) + mstate.shoot(mstate.but_adv())
		

		
