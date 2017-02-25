#les objets de base
from soccersimulator import Vector2D, SoccerState, SoccerAction

#objets pour un match
from soccersimulator import Simulation, SoccerTeam, Player, show_simu, SoccerTournament

#importer la strategie de base
from soccersimulator import Strategy

#toutes les constantes
from soccersimulator import settings

#toutes les tactiques
from tactic import TTactic, FTactic, STactic
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
		sens = 1
		pos = 50
		if idteam == 1 :
			sens = 1
			pos = 100
		else:
			sens = -1
			pos = 50
		coeq = mstate.coeq_nearby
		
		"""une variable qui va etudier cas : 1-si l'adversaire est plus proche de la balle que nous on va en defense
		sinon on a 2-notre jouer le + proche -> va a la balle et fait une action
		l'action passe s'il est en defense et tir vers les buts sinon
		et l'autre joueur avance vers la balle si l'autre joueur est en defense sinon va vers les buts'
		"""
		#return mstate.adv_nearby
		if mstate.key[1] == 0:
			me_b = mstate.my_position.distance(mstate.ball_position)
			other_b = coeq.distance(mstate.ball_position)
			
			me_g = mstate.my_position.distance(mstate.but_adv)
			other_g = coeq.distance(mstate.but_adv)
			if me_b < other_b:#si je suis plus proche de la balle que l'autre
				if me_g < other_g:# si je suis plus proche des but que lui
					return mstate.aller_ball + mstate.shoot(mstate.but_adv)
				return mstate.aller_ball + mstate.shoot(coeq)
			
			if mstate.my_position.x*sens < pos*sens :
				return mstate.aller(mstate.my_position + sens*Vector2D(10, 0)) 
		#si adv + proche est a x > 50
		#mstate.state.player_state(adv[0], adv[1]).position.x*sens > sens*pos
		
		elif mstate.my_position.distance(coeq) > 10:
			if mstate.can_shoot :
				return mstate.shoot(mstate.state.player_state(mstate.key[0], 0).position)
			return mstate.aller_ball
		"""elif mstate.my_position.distance(mstate.ball_position) > 1:
			return mstate.aller(mstate.ball_position) + mstate.shoot(mstate.but_adv)	
		"""		
		
		adv_w_ball = mstate.adv_players[0] if mstate.adv_players[0].distance(mstate.ball_position) < mstate.adv_players[1].distance(mstate.ball_position) else mstate.adv_players[1]
			
		return mstate.aller(adv_w_ball)

class SoloStrat(Strategy):
	def __init__(self, name="soloStrategy"):
		Strategy.__init__(self, name)
	def compute_strategy(self, state, idteam, idplayer):
		mstate = MyState(state, idteam, idplayer)
		
		sens = 1 if idteam == 1 else -1
		
		me = mstate.my_position
		adv = mstate.adv_players[0]
		ball = mstate.ball_position
		but_adv = mstate.but_adv
		but = mstate.but
		
		if me.distance(ball) < adv.distance(ball) :#and me.distance(but_adv) > adv.distance(but_adv):
			if mstate.adv_on_right*sens > 0 :
				if me.distance(but_adv) < adv.distance(but_adv) :
					return mstate.aller_ball + mstate.shoot(but_adv*0.001)
				return mstate.aller_ball + mstate.shoot(but_adv)
			return mstate.aller_ball + mstate.shoot(but_adv*0.001)
				
		return mstate.aller_ball + mstate.shoot(but_adv)
		"""		if me.distance(but_adv) > 10 :
					return mstate.aller(ball) + mstate.shoot(me + Vector2D(1, 1))
				elif me.distance(but_adv) > 10 :#and me.distance(but_adv) > adv.distance(but_adv) :
					return mstate.aller(ball) + mstate.shoot(me + sens*Vector2D(1, 1))
				return mstate.aller(ball) + mstate.shoot(but_adv)
			elif me.distance(but_adv) > 10 :
					return mstate.aller(ball) + mstate.shoot(me + sens*Vector2D(1, 1))
			return mstate.aller(ball) + mstate.shoot(but_adv)
		else :
			return mstate.aller(ball) + mstate.shoot(but + Vector2D(40, 0))
		"""
class Solo(Strategy):
	def __init__(self, name="soloStrategy"):
		Strategy.__init__(self, name)
	def compute_strategy(self, state, idteam, idplayer):
		mstate = MyState(state, idteam, idplayer)
		
		sens = 1 if idteam == 1 else -1
		
		me = mstate.my_position
		adv = mstate.state.player_state(mstate.adv_players[0][0], mstate.adv_players[0][1]).position
		ball = mstate.ball_position
		but_adv = mstate.but_adv
		but = mstate.but
		tirer_but = mstate.aller(ball) + mstate.shoot(but_adv)
		"""
		va vers la balle si l'autre joueur adverse a dist = ou plus grande que moi a la balle
		si la balle dans ma defense : sinon s'il a un x inferieur a l'adversaire il defend en restant entre le but et la balle, et si la balle est plus proche de moi je fonce et tire dans ma direction de course quand je pourrais shooter
		...
		...
		"""
		if me.distance(ball) <= adv.distance(ball) :
			if (sens == 1 and ball.x > 75) or (sens == -1 and ball.x < 75) :
				return tirer_but
			else :
				return tirer_but 
		else :
			if (sens == 1 and ball.x > 75) or (sens == -1 and ball.x < 75) : 
				return tirer_but
			else :	
				return mstate.aller((but + adv * 5) / 6)
					
		
		
class AttaquantPlus(Strategy):
	def __init__(self, name="attaquantPlus"):
		Strategy.__init__(self, name)
	def compute_strategy(self, state, idteam, idplayer):
		mstate = MyState(state, idteam, idplayer)
		
		for p in mstate.co_players:
	#if un autre joueur proche de la balle et la balle au dela de la moitie du terrain aller de lavant
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
		if mstate.my_position.distance(mstate.ball_position) < mstate.my_position.distance(mstate.adv_nearby):
			return mstate.aller(mstate.ball_position) + mstate.shoot(mstate.but_adv)

		#
		return mstate.aller(mstate.adv_nearby - Vector2D(0,0))
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
		p = mstate.adv_nearby
		if mstate.my_position.distance(mstate.ball_position) < mstate.my_position.distance(mstate.state.player_state(p[0], p[1]).position):
			p = mstate.coeq_nearby
			return mstate.aller(mstate.ball_position) + mstate.shoot(mstate.state.player_state(p[0], p[1]).position)

		return mstate.aller(mstate.state.player_state(p[0], p[1]).position)
		#return mstate.aller(mstate.ball_position()) + mstate.shoot(mstate.but_adv())
		
class Tireur(object):
	def __init__(self, name, k):
		self.k = k
		Strategy.__init__(self, name)
	def compute_strategy(self, state, idteam, idplayer):
		mstate = MyState(state, idteam, idplayer)
		
		return mstate.tirer(mstate.but_adv, self.k)
		
		
#strategie avec tactics
class Strat(Strategy):
	#strategie attaque 2v2 utilisant des tactiques en fction de la situation
	def __init__(self, name="attack"):
		Strategy.__init__(self, name)
	def compute_strategy(self, state, idteam, idplayer):
		mstate = MyState(state, idteam, idplayer)
		tactic = TTactic(state, idteam, idplayer)
		
		
		advs = mstate.adv_players	#tous les adversaires
		coes = mstate.co_players	#tous les coequipiers
		
		return tactic.attaquer
		
class SoloTac(Strategy):
	#strategie attaque 2v2 utilisant des tactiques en fction de la situation
	def __init__(self, name="attack"):
		Strategy.__init__(self, name)
	def compute_strategy(self, state, idteam, idplayer):
		mstate = MyState(state, idteam, idplayer)
		tactic = STactic(state, idteam, idplayer)
		
		
		return tactic.attaquer

class StratRien(Strategy):
	#strategie attaque 2v2 utilisant des tactiques en fction de la situation
	def __init__(self, name="attack"):
		Strategy.__init__(self, name)
	def compute_strategy(self, state, idteam, idplayer):
		mstate = MyState(state, idteam, idplayer)
		tactic = STactic(state, idteam, idplayer)
		
		
		return SoccerAction(Vector2D(), Vector2D())
		
class Shooter(Strategy):
	def __init__(self, name="shooter"):
		Strategy.__init__(self, name)
	def compute_strategy(self, state, idteam,idplayer):
		mstate = MyState(state, idteam, idplayer)
		
		k = mstate.my_position.distance(mstate.ball_position)
		#def shoot(self, k):
		return SoccerAction(Vector2D(), math.exp(k)*(mstate.but_adv - mstate.my_position))
		
		"""class Shooter(Strategy):
	def __init__(self, name="shooter"):
		Strategy.__init__(self, name)
	def compute_strategy(self, state, idteam,idplayer):
		mstate = MyState(state, idteam, idplayer, k)
		return SoccerAction(Vector2D(), k*(mstate.but_adv - mstate.my_position))
		"""
		
		
