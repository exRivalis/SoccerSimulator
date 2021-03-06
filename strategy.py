#les objets de base
from soccersimulator import Vector2D, SoccerState, SoccerAction, KeyboardStrategy

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

class Shooter(Strategy):
	def __init__(self, name="shooter"):
		Strategy.__init__(self, name)
	def compute_strategy(self,state, idteam, idplayer):
		mstate = MyState(state,idteam,idplayer)
		return mstate.shoot(mstate.but_adv)
		
class Passeur(Strategy):
	def __init__(self, name="Passer"):
		Strategy.__init__(self, name)
	def compute_strategy(self,state, idteam, idplayer):
		mstate = MyState(state,idteam,idplayer)
		co = mstate.co_danger_but()
		co_pos = mstate.state.player_state(co[0], co[1]).position
		co_dist = co_pos.distance(mstate.my_position)
		if co_dist < 65 :
			return mstate.shoot(co_pos)
		else :
			co = mstate.coeq_nearby()
			return mstate.shoot(mstate.state.player_state(co[0], co[1]))

class GardienB(Strategy):
	def __init__(self, name="GardienB"):
		Strategy.__init__(self, name)
	def compute_strategy(self,state, idteam, idplayer):
		mstate = MyState(state, idteam, idplayer)
		
		#print mstate.ball_position
		#mstate.predict_ball
	
		sens = 1 if idteam == 1 else -1
		
		me = mstate.my_position
		adv = mstate.state.player_state(mstate.adv_nearby()[0], mstate.adv_nearby()[1]).position
		#(mstate.adv_nearby())
		ball = mstate.ball_position
		but_adv = mstate.but_adv
		but = mstate.but
		
		y_move = ((ball.y-45) * 15)/abs(ball.x - but.x) if abs(ball.x-but.x)>3 else 0
		pos_init = Vector2D(10, 45) if idteam == 1 else Vector2D(140, 45)
		pos_base = pos_init + Vector2D(0, y_move) 
		cote_attaque = (sens == 1 and ball.x > 75) or (sens == -1 and ball.x < 75)
		cote_defense = (sens == 1 and ball.x > 75) or (sens == -1 and ball.x < 75)
		adv_dist = me.distance(adv)
		si_sort = True if (me.distance(ball) < (adv.distance(ball)+2*mstate.v_ball.norm) and ball.distance(but)<75) else False
		si_avance = True if (me.distance(ball) < 2 * adv.distance(ball) and ball.distance(but)<35) else False
		#l'adversaire plus proches aux buts que le gardien
		adv_but = [p for p in mstate.adv_players if (mstate.state.player_state(p[0],p[1]).position.distance(but) < me.distance(ball))]
		#s'il y a un adversaire plus proche des buts que moi
		adv_danger = False if adv_but == [] else True
		co = mstate.coeq_libre if mstate.coeq_libre !=[0, 0] else mstate.co_players[0] 
		co_pos = mstate.state.player_state(mstate.co_players[0][0], mstate.co_players[0][1]).position
		
		#normalement dans le else je met le plus proche
		
		pos_coeq_libre = mstate.state.player_state(co[0], co[1]).position
		
		me_but_mine = mstate.my_position.distance(mstate.but)
		me_but = mstate.my_position.distance(mstate.but_adv)
		
		passer = mstate.shoot(pos_coeq_libre)
	
		joue = mstate.shoot(pos_coeq_libre) if mstate.coeq_libre != [0, 0] else mstate.degager
		
		me_ball = me.distance(ball+mstate.v_ball*10)
		co_ball = co_pos.distance(mstate.ball_position+mstate.v_ball*10)
		adv = mstate.adv_danger_but()
		pos_adv = mstate.state.player_state(adv[0], adv[1]).position
		pos_contre = pos_adv + Vector2D(-11,0) if sens == 1 else pos_adv + Vector2D(11, 0)
		adv_ball = pos_adv.distance(mstate.ball_position+mstate.v_ball*10)
		
		
		
		if mstate.closest_ball: #si je suis le plus proche de tous de la balle
			if me_but < 45:
				return mstate.shoot(mstate.but_adv)
			if me_but_mine < 43: #ma distance a mes buts
				return mstate.degager
			if mstate.champs_libre:
				return mstate.go_but
			return mstate.passe(co_pos)
		if mstate.our_ball:
			return mstate.aller(pos_contre)
		if (si_sort == True) :
			return joue
		elif (si_avance == True) :
			return mstate.aller((ball-mstate.my_position)/4+ mstate.my_position)
		return mstate.aller(pos_base)



class Defense(Strategy):
	def __init__(self, name="defense"):
		Strategy.__init__(self, name)
	def compute_strategy(self,state, idteam, idplayer):
		mstate = MyState(state,idteam,idplayer)
		adv = mstate.state.player_state(mstate.adv_nearby()[0], mstate.adv_nearby()[1]).position
		co = mstate.coeq_libre if mstate.coeq_libre !=[0, 0] else mstate.co_players[0] 
		co_pos = mstate.state.player_state(mstate.co_players[0][0], mstate.co_players[0][1]).position
		me_ball = mstate.my_position.distance(mstate.ball_position+mstate.v_ball*10)
		co_ball = co_pos.distance(mstate.ball_position+mstate.v_ball*10)
		adv = mstate.adv_danger_but()
		pos_adv = mstate.state.player_state(adv[0], adv[1]).position
		pos_contre = pos_adv + Vector2D(-11,0) if mstate.sens == 1 else pos_adv + Vector2D(11, 0)
		adv_ball = pos_adv.distance(mstate.ball_position+mstate.v_ball*10)
		but_adv = mstate.but_adv
		but = mstate.but
		ball_but = mstate.ball_position.distance(but)
		ball_but_adv = mstate.ball_position.distance(but_adv)
		adv = mstate.state.player_state(mstate.adv_nearby()[0], mstate.adv_nearby()[1]).position
		adv_speed = mstate.state.player_state(mstate.adv_nearby()[0], mstate.adv_nearby()[1]).vitesse
		pos_init = Vector2D(adv.x- (10 * mstate.sens), 45)
		y_move = (((adv.y -45) * abs(adv.x - 10*mstate.sens)) / abs(adv.x -but.x)) if abs(adv.x -but.x) > 3 else 0
				
		pos_base = pos_init + Vector2D(0, y_move)
		"""if me_ball < adv_ball:
			return mstate.shoot(co_pos)
		elif adv.x < 11 and mstate.sens == 1 or :"""
		return mstate.aller(pos_base)
		
		"""if (adv_danger == True) :
			if mstate.my_position !=pos_base :
				return mstate.aller(pos_base)
			else :	
				return joue
		if (si_sort == True) :
			return joue
		#si l'adversaire est assez proche
		elif (si_avance == True) :
			return mstate.aller(ball/4)
		else :
			return mstate.aller(pos_base)"""
#4vs4:
#defenseur derriere
#il va vers la balle pour l'enlever s'il est le plus proche d'elle ou que je suis le plus proche de mes coeq a cet adversaire, sinon je vais surveiller l'avant dernier de leurs attaquants, si la balle est a nous alor je me positionne entre mes 2 coeq attaquants legerement derriere
class Defense1(Strategy):
	def __init__(self, name="defense1"):
		Strategy.__init__(self, name)
	def compute_strategy(self,state, idteam, idplayer):
		mstate = MyState(state,idteam,idplayer)
		sens = mstate.sens
		adv_near = mstate.state.player_state(mstate.adv_nearby()[0], mstate.adv_nearby()[1]).position
		ball_adv_near = mstate.ball_position.distance(adv_near)
		co = mstate.coeq_libre if mstate.coeq_libre !=[0, 0] else mstate.co_players[0] 
		co_pos = mstate.state.player_state(co[0], co[1]).position
		me_ball = mstate.dist_ball
		co_ball = co_pos.distance(mstate.ball_position+mstate.v_ball*10)
		adv_danger2 = mstate.adv_danger2_but() 
		pos_adv_danger2 = mstate.state.player_state(adv_danger2[0], adv_danger2[1]).position
		pos_contre = pos_adv_danger2 + Vector2D(-11,0) if mstate.sens == 1 else pos_adv_danger2 + Vector2D(11, 0)
		adv_ball = pos_adv_danger2.distance(mstate.ball_position+mstate.v_ball*10)
		but_adv = mstate.but_adv
		but = mstate.but
		ball_but = mstate.ball_position.distance(but)
		ball_but_adv = mstate.ball_position.distance(but_adv)
		adv = mstate.state.player_state(mstate.adv_nearby()[0], mstate.adv_nearby()[1]).position
		adv_speed = mstate.state.player_state(mstate.adv_nearby()[0], mstate.adv_nearby()[1]).vitesse
		pos_init = Vector2D(adv.x- (10 * mstate.sens), 45)
		y_move = (((adv_near.y -45) * abs(adv_near.x - 10*mstate.sens)) / abs(adv_near.x -but.x)) if abs(adv_near.x -but.x) > 3 else 0
		
		me_but_mine = mstate.dist_but_mine
		me_but = mstate.dist_but_adv
		
		"""if me_ball < adv_ball:
			return mstate.shoot(co_pos)
		elif adv.x < 11 and mstate.sens == 1 or :"""
		att1 = mstate.co_danger_but()
		att2 = mstate.co_danger2_but()
		att1_pos = mstate.state.player_state(att1[0], att1[1]).position
		att2_pos = mstate.state.player_state(att2[0], att2[1]).position
		pos_att = (((att1_pos+att2_pos)/2) + Vector2D(-10,0)) if sens ==1 else (((att1_pos+att2_pos)/2) + Vector2D(10,0))
		adv_2 = mstate.adv_danger2_but()
		pos_def = mstate.state.player_state(adv_2[0], adv_2[1]).position + Vector2D(-5, 0) if sens ==1 else mstate.state.player_state(adv_2[0], adv_2[1]).position + Vector2D(5, 0)
		diff = att2_pos - adv_near
		move = diff/15
		pos_def_off = mstate.my_position + move
		if mstate.closest_ball: #si je suis le plus proche de tous de la balle
			if me_but < 35:
				return mstate.shoot(mstate.but_adv)
			if me_but_mine < 43: #ma distance a mes buts
				return mstate.degager
			if mstate.champs_libre:
				return mstate.go_but
			return mstate.passe(co)
		if mstate.our_ball:
			return mstate.aller(pos_att)
		if me_ball < ball_adv_near or (mstate.plus_proche and me_but_mine < 85):
			return mstate.aller(pos_def_off)
		return mstate.aller(pos_def)
		
		
		
#4vs4:
#attaquant2:
class Atta2(Strategy):
	def __init__(self, name="att2"):
		Strategy.__init__(self, name)
	def compute_strategy(self, state, idteam, idplayer):
		mstate = MyState(state, idteam, idplayer)
		me_but_mine = mstate.dist_but_mine
		me_but = mstate.dist_but_adv
		me_ball = mstate.dist_ball
		co = mstate.coeq_nearby()
		co_pos = mstate.state.player_state(co[0], co[1]).position
		#mon premier attaquant et sa position
		att1 = mstate.co_danger_but()
		att1_pos = mstate.state.player_state(att1[0], att1[1]).position
		def_adv = mstate.adv_dernier_def
		def_adv_pos = mstate.state.player_state(def_adv[0], def_adv[1]).position
		pos_att = Vector2D(def_adv_pos.x, 45 - (45-co_pos.y))
		def2_adv = mstate.adv_def2
		def2_adv_pos = mstate.state.player_state(def2_adv[0], def2_adv[1]).position
		adv_att2 = mstate.adv_danger2_but()
		adv_att2_pos = mstate.state.player_state(adv_att2[0], adv_att2[1]).position
		pos_contre = adv_att2_pos + Vector2D(10, 0) if mstate.sens == 1 else adv_att2_pos + Vector2D(-10, 0)
		if mstate.closest_ball:
			if me_but < 35:
				return mstate.shoot(mstate.but_adv)
			if me_but_mine < 43: #ma distance a mes buts
				return mstate.degager
			if mstate.champs_libre:
				return mstate.go_but
			return mstate.passe(co)
		if mstate.our_ball:
			return mstate.aller(pos_att)
		#la balle en attaque
		if mstate.ball_position.distance(mstate.but) > 75:
			return mstate.aller_ball
		#sinon dans ma defense
		return mstate.aller(pos_contre)
		
		
#4vs4
class Attaqtaq(Strategy):
	def __init__(self, name="attaquant2"):
		Strategy.__init__(self, name)
	def compute_strategy(self, state, idteam, idplayer):
		ms = MyState(state, idteam, idplayer)
		
		adv = ms.adv_nearby()
		sens = ms.sens
		coeq = ms.coeq_nearby()
		
		if ms.have_ball:
			if ms.state.player_state(adv[0], adv[1]).position.x*sens < ms.my_position.x*sens:#adv le plus proche derrier: foncer but
				return ms.go_but
			#sinon si je suis le plus proche des buts je fonce
			if ms.plus_proche_but:
				return ms.go_but
		#si j'ai pas la balle et aucun de mes coeq n'a la balle je fonce vers la balle 
		co_pball = ms.co_pball()
		#si je nesuis pas le plus prochede la balle je monte en attaque
		#si la balle est dans mon camp je descend sinon je vais en attaque
		if ms.ball_position.x*sens < 45:
			return ms.aller_ball
		elif ms.state.player_state(co_pball[0], co_pball[1]).position != ms.my_position:
			return ms.aller(ms.but_adv - sens*Vector2D(-10, -5))
		return ms.aller_ball
#creation strategy
class Attaquant(Strategy):
	
	def __init__(self, name="Attaquant"):
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
		#mon coeq plus proche de la balle alor j'attend la balle j'y vais pas
		me_ball = mstate.my_position.distance(mstate.ball_position+mstate.v_ball*5)
		co_ball = mstate.state.player_state(mstate.co_players[0][0], mstate.co_players[0][1]).position.distance(mstate.ball_position+mstate.v_ball*5)
		adv = mstate.adv_danger_but()
		pos_adv = mstate.state.player_state(adv[0], adv[1]).position
		pos_contre = pos_adv + Vector2D(25,0) if sens == 1 else pos_adv + Vector2D(-25, 0)
		adv_ball = pos_adv.distance(mstate.ball_position+mstate.v_ball)
		if me_ball > co_ball:
			return mstate.aller(pos_contre)
		
		if mstate.my_position.distance(mstate.but_adv) >30 :
			if mstate.my_position.distance(mstate.state.player_state(adv[0], adv[1]).position) < 15 :
				return mstate.drible()
			return mstate.go_but
		return mstate.shoot(mstate.but_adv)
		

class SoloStrat(Strategy):
	def __init__(self, name="soloStrategy"):
		Strategy.__init__(self, name)
	def compute_strategy(self, state, idteam, idplayer):
		mstate = MyState(state, idteam, idplayer)
		dist = mstate.dist_ball
		v_ball = mstate.v_ball
		
		return mstate.aller(mstate.ball_position) + mstate.tirer

class SoloStrat(Strategy):
	def __init__(self, name="soloStrategy"):
		Strategy.__init__(self, name)
	def compute_strategy(self, state, idteam, idplayer):
		mstate = MyState(state, idteam, idplayer)
		return mstate.aller(mstate.but_adv) + mstate.shoot(mstate.but_adv)
		"""sens = 1 if idteam == 1 else -1
		
		me = mstate.my_position
		adv = mstate.state.player_state(mstate.adv_players[0][0], mstate.adv_players[0][1]).position
		ball = mstate.ball_position
		but_adv = mstate.but_adv
		but = mstate.but
		
		if me.distance(ball) < adv.distance(ball) :#and me.distance(but_adv) > adv.distance(but_adv):
			if mstate.adv_on_right*sens > 0 :
				if me.distance(but_adv) < adv.distance(but_adv) :
					return mstate.aller(ball) + mstate.shoot(but_adv*0.001)
				return mstate.aller(ball) + mstate.shoot(but_adv)
			return mstate.aller(ball) + mstate.shoot(but_adv*0.001)
				
		return mstate.aller(ball) + mstate.shoot(but_adv)"""
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
		adv = mstate.adv_players
		sens = 1
		if adv[0] == 1 :
			sens = 1
		else:
			sens = -1
		adv_pos = mstate.state.player_state(adv[0][0], adv[0][1]).position
		me = mstate.my_position
		if mstate.my_position.distance(mstate.but_adv) >30 :
			if mstate.my_position.distance(mstate.state.player_state(adv[0][0], adv[0][1]).position) < 15 :
				if mstate.my_position.distance(mstate.state.player_state(adv[0][0], adv[0][1]).position) < 3 :
					return mstate.shoot(mstate.but_adv)
				return mstate.drible()
			return mstate.go_but
		return mstate.shoot(mstate.but_adv)
		
					
		
		
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
		
class Gardien(Strategy):
	def __init__(self, name = "Gardien"):
		Strategy.__init__(self, name)
	def compute_strategy(self, state, idteam, idplayer):
		mstate = MyState(state, idteam, idplayer)
		
		#print mstate.ball_position
		#mstate.predict_ball
	
		sens = 1 if idteam == 1 else -1
		
		me = mstate.my_position
		adv = mstate.state.player_state(mstate.adv_nearby()[0], mstate.adv_nearby()[1]).position
		#(mstate.adv_nearby())
		ball = mstate.ball_position
		but_adv = mstate.but_adv
		but = mstate.but
		
		y_move = ((ball.y-45) * 15)/abs(ball.x - but.x) if abs(ball.x-but.x)>3 else 0
		pos_init = Vector2D(10, 45) if idteam == 1 else Vector2D(140, 45)
		pos_base = pos_init + Vector2D(0, y_move) 
		cote_attaque = (sens == 1 and ball.x > 75) or (sens == -1 and ball.x < 75)
		cote_defense = (sens == 1 and ball.x > 75) or (sens == -1 and ball.x < 75)
		adv_dist = me.distance(adv)
		si_sort = True if (me.distance(ball) < (adv.distance(ball)+2*mstate.v_ball.norm) and ball.distance(but)<75) else False
		si_avance = True if (me.distance(ball) < 2 * adv.distance(ball) and ball.distance(but)<35) else False
		#l'adversaire plus proches aux buts que le gardien
		adv_but = [p for p in mstate.adv_players if (mstate.state.player_state(p[0],p[1]).position.distance(but) < me.distance(ball))]
		#s'il y a un adversaire plus proche des buts que moi
		adv_danger = False if adv_but == [] else True
		co = mstate.coeq_libre if mstate.coeq_libre !=[0, 0] else mstate.co_players[0] 
		co_pos = mstate.state.player_state(mstate.co_players[0][0], mstate.co_players[0][1]).position
		#normalement dans le else je met le plus proche
		
		pos_coeq_libre = mstate.state.player_state(co[0], co[1]).position
		
		
		passer = mstate.shoot(pos_coeq_libre)
	
		joue = mstate.shoot(pos_coeq_libre) if mstate.coeq_libre != [0, 0] else mstate.degager
		
		me_ball = me.distance(ball+mstate.v_ball*10)
		co_ball = co_pos.distance(mstate.ball_position+mstate.v_ball*10)
		adv = mstate.adv_danger_but()
		pos_adv = mstate.state.player_state(adv[0], adv[1]).position
		pos_contre = pos_adv + Vector2D(-11,0) if sens == 1 else pos_adv + Vector2D(11, 0)
		adv_ball = pos_adv.distance(mstate.ball_position+mstate.v_ball*10)
		
		if co_ball < adv_ball and ball.distance(but) > 65:
			if me_ball < co_ball:
				return mstate.shoot(co_pos)
			else :
				return mstate.aller(pos_contre)
		
		if (adv_danger == True) :
			if mstate.my_position !=pos_base :
				return mstate.aller(pos_base)
			else :	
				return joue
		if (si_sort == True) :
			return joue
		#si l'adversaire est assez proche
		elif (si_avance == True) :
			return mstate.aller(ball/4)
		else :
			return mstate.aller(pos_base)
# implementer quand le gardien sort, et son emplacement quand la balle est en defense et pour les defenseur et attaquants retour passe derriere au plus proche libre 



class Def(Strategy):
	def __init__(self, name = "def"):
		Strategy.__init__(self, name)
	def compute_strategy(self, state, idteam, idplayer):
		mstate = MyState(state, idteam, idplayer)
	
	
		sens = 1 if idteam == 1 else -1
		
		me = mstate.my_position
		adv = mstate.state.player_state(mstate.adv_nearby()[0], mstate.adv_nearby()[1]).position
		#(mstate.adv_nearby())
		ball = mstate.ball_position
		but_adv = mstate.but_adv
		but = mstate.but
		y_move = ((ball.y-45) * 15)/abs(ball.x - but.x)
		pos_init = Vector2D(10, 45) if idteam == 1 else Vector2D(140, 45)
		pos_base = pos_init + Vector2D(0, y_move) 
		cote_attaque = (sens == 1 and ball.x > 75) or (sens == -1 and ball.x < 75)
		cote_defense = (sens == 1 and ball.x > 75) or (sens == -1 and ball.x < 75)
		adv_dist = me.distance(adv)
		si_sort = True if (me.distance(ball) < adv.distance(ball) and ball.distance(but)<75) else False
		si_avance = True if (me.distance(ball) < 2 * adv.distance(ball) and ball.distance(but)<35) else False
		degager = mstate.shoot(but_adv)
		#l'adversaire plus proches aux buts que le gardien
		adv_but = [p for p in mstate.adv_players if (mstate.state.player_state(p[0],p[1]).position.distance(but) < me.distance(ball))]
		#s'il y a un adversaire plus proche des buts que moi
		adv_danger = False if adv_but == [] else True
		co = mstate.coeq_libre if mstate.coeq_libre !=[0, 0] else mstate.co_players[0] 
		#normalement dans le else je met le plus proche
		
		pos_coeq_libre = mstate.state.player_state(co[0], co[1]).position
		
		
		passer = mstate.shoot(pos_coeq_libre)
	
		joue = mstate.shoot(pos_coeq_libre) if mstate.coeq_libre != [0, 0] else degager
		
		if true:
			if (adv_danger == True) :
				return mstate.aller(pos_base)
			if (si_sort == True) :
				return joue
			#si l'adversaire est assez proche
			elif (si_avance == True) :
				return mstate.aller_ball
			else :
				return mstate.aller(pos_base)



"""
import logging
logger = logging.getLogger("name")
logger.info("")
		.debug
		.warning
logger.basicConfig(level = logging.INFO)
"""
class StratARien(Strategy):
	def __init__(self, name = "sert_a_rien"):
		Strategy.__init__(self, name)
	def compute_strategy(self, state, idteam, idplayer):
		mstate = MyState(state, idteam, idplayer)
		
		return SoccerAction(Vector2D(0,0), Vector2D())

#dribleur
class Dribbleur(Strategy):
	def __init__(self, name = "dribbleur"):
		Strategy.__init__(self, name)
	def compute_strategy(self, state, idteam, idplayer):
		ms = MyState(state, idteam, idplayer)
		sens = ms.sens
		
		#recup advs devant moi
		advs = [p for p in ms.adv_players if ms.state.player_state(p[0], p[1]).position.x*sens > ms.my_position.x*sens]
		
		#s'il n'y a personne devant
		if len(advs) == 0:
			return ms.shoot(ms.but_adv)
		#je recup le plus proche d'ntre eux
		p = advs[0]
		for i in advs:
			if ms.my_position.distance(ms.state.player_state(i[0], i[1]).position) < ms.my_position.distance(ms.state.player_state(p[0], p[1]).position):
				p = i
				
		#s'il y a quelqu'un sur mon chemin a droite je vais a gauche et inversement
		dy = (ms.my_position.y - ms.state.player_state(p[0], p[1]).position.y)
		ball = ms.ball_position
		if ms.can_shoot == False:
			return ms.shoot(ms.my_position + Vector2D(10, dy))
		if abs(dy) < 10:#aller en haut ou en bas
			return ms.shoot(ms.but_adv)
			#SoccerAction(ms.my_position + Vector2D(10, dy), Vector2D()) + SoccerAction(Vector2D(), ball)
		#aller droit vers les buts
		return ms.shoot(ms.but_adv)
		
#changement de strategies avec le clavier

