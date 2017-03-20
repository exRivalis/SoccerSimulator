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
		self.but = Vector2D(0, 45) if self.key[0] == 1 else Vector2D(150, 45)
		#recup joueur sous forme n-uplets 
		self.all_players = self.state.players
		
		self.co_players = [p  for p in self.all_players if (p[0] == self.key[0] and p[1] != self.key[1])]
				
		self.adv_players = [p  for p in self.all_players if p[0] != self.key[0]]
		
		#can the player shoot in the ball
		self.can_shoot = True if self.my_position.distance(self.ball_position) < 0.82 else False
		#nouvelles motif pour simplifier
		self.sens = 1 if self.key[0] == 1 else -1
		
		#print self.state.states, "\n"
		
		
		
		#side of adv
		self.adv_on_right = 1 if self.state.player_state(self.adv_players[0][0], self.adv_players[0][1]).position.y > self.my_position.y else -1
		
		#vitesse balle
		self.v_ball = self.state.ball.vitesse
		
		#distance de la balle
		self.dist_ball = self.my_position.distance(self.ball_position)
		
		
		
		#mon vecteur vitesse
		self.my_v = self.state.player_state(self.key[0], self.key[1]).vitesse
		
		#est proche de la balle
		self.near_ball = True if self.my_position.distance(self.ball_position) < 20 else False
		
		#liste des coeq proche
		self.coeq_proche = [p for p in self.co_players if self.my_position.distance(self.state.player_state(p[0], p[1]).position) < 75]
		
	
	#return les players avec leurs caracs
	@property
	def me(self):
		return self.state.player_state(self.key[0], self.key[1])
		
	@property
	def all_players_p(self):	
		#renvoie tous les joueurs avec toutes leur carac
		players = [self.state.player_state(p[0], p[1]) for p in self.state.players]
		return players
	
	@property
	def co_players_p(self):
		#self.co_players_p = [p  for p in self.all_players_p if (p.key[0] and p[1] != self.key[1])]
		co = [self.state.player_state(p[0], p[1]) for p in self.state.players if p[0] == self.key[0] and p[1] != self.key[1]]
		return co	
	
	@property
	def adv_players_p(self):
		#self.co_players_p = [p  for p in self.all_players_p if (p.key[0] and p[1] != self.key[1])]
		co = [self.state.player_state(p[0], p[1]) for p in self.state.players if p[0] != self.key[0]]
		return co
	
	@property
	def adv_nearby_p(self):
		adv = self.adv_players_p[0]
		for p in self.adv_nearby_p:
			dist_p = p.position.distance(self.my_position)
			dist_adv = adv.position.distance(self.my_position)
			if dist_p < dist_adv:
				adv = p
		return adv
		
	@property
	def coeq_nearby_p(self):
		coeq = self.co_players_p[0]
		for p in self.adv_nearby_p:
			dist_p = p.position.distance(self.my_position)
			dist_coeq = coeq.position.distance(self.my_position)
			if dist_p < dist_coeq:
				coeq = p
		return coeq
	
	
	@property
	def coeq_libre(self) :
		if len(self.coeq_proche) == 0 :
			return [0, 0]
		elif len(self.coeq_proche) == 1 :
			return self.coeq_proche[0]
		else :
			x = mstate.player_state(p[0], p[1]).position.distance(mstate.player_state(p[0], p[1]).adv_nearby())
			pp = coeq_proche[0]
			for p in coeq_proche[1:] :
				d = mstate.player_state(p[0], p[1]).position.distance(mstate.player_state(p[0], p[1]).adv_nearby())
				if x < d :
					x = d
					pp = p
			return pp
	@property
	def aller_ball(self) :
		#les cas ou je suis proche de la balle et elle va vite?
		v_ball = self.v_ball
		dist = self.dist_ball
		if self.my_position.distance(self.ball_position) > 10:
			return SoccerAction((math.exp(dist)*v_ball +(self.ball_position - self.my_position)), Vector2D())
		elif self.my_position.distance(self.ball_position) > 5:
			return SoccerAction((math.exp(dist)*v_ball +(self.ball_position - self.my_position))/2, Vector2D())
		else :
			SoccerAction((self.ball_position-self.my_position).normalize()  , Vector2D())
	
	
	def aller(self, p) :
		self.all_players_p
		dist = p.distance(self.my_position)
		v_ball = self.v_ball
		vec_dest = p-self.my_position
		if dist < 10:
			return SoccerAction((dist/4)*vec_dest, Vector2D())
		return SoccerAction((math.exp(dist-10))*vec_dest, Vector2D())
		
	
	def shoot(self, p) :
		k = p.distance(self.my_position)
		if self.can_shoot :
			if self.my_position.distance(p) < 20 : 				
				return SoccerAction(Vector2D(),(p-self.my_position)/2)
			return SoccerAction(Vector2D(), math.exp(k)*(p-self.my_position))  
		else :
			return self.aller(self.ball_position)
	
	@property
	def tirer(self):
		k = self.my_position.distance(self.ball_position)
		if self.can_shoot:
			if self.my_position.distance(self.ball_position) < 10:
				return SoccerAction(Vector2D(), math.exp(k/2)*(self.but_adv - self.my_position))
			return SoccerAction(Vector2D(), (self.but_adv - self.my_position)*(self.but_adv - self.my_position)/300)
			#SoccerAction(Vector2D(), math.exp(k/2)*(self.but_adv - self.my_position))
		return SoccerAction(Vector2D(), Vector2D())
	"""
	@property
	def attaque_droite(self):
		if self.state.player_state(self.coeq_nearby[0], self.coeq_nearby[1]).position.distance(self.my_position) > 20:
			self.aller(self.ball_position) + shoot(self.state.player_state(self.coeq_nearby[0], self.coeq_nearby[1]).position) + 
		"""
		
	#recup adv le plus proche
	#@property
	def adv_nearby(self):
		players = self.adv_players
		"""if len(players) == 1:
			return None"""
		pp = players[0]
		for p in players:
			#print self.my_position.distance(self.state.player_state(p[0], p[1]).position)
			#print self.my_position.distance(self.state.player_state(pp[0], pp[1]).position)
			if self.my_position.distance(self.state.player_state(p[0], p[1]).position) < self.my_position.distance(self.state.player_state(pp[0], pp[1]).position):
				pp = p
		return pp
	
	def pos_j(self, p):
		return self.state.player_state(p[0], p[1]).position
		
	def passe(self, p):
		j_pos = self.pos_j(p)
		dist = self.my_position.distance(j_pos) 
		#k = dist/ 
		player = self.state.player_state(p[0], p[1])
		v_p = player.vitesse
		vect =( j_pos + math.exp(dist/15)*v_p ) - self.my_position
		print dist
		return SoccerAction(Vector2D(), vect)
	
	
	def adv_nearbyj(self, idteam, idplayer) :
		if self.idteam == idteam :
			return adv_nearby()
		else :
			return coeq_nearby()
		
	
		#recup adv le plus proche
	def coeq_nearby(self):
		
		players = self.co_players
		"""if len(players) == 1:
			return """
		pp = players[0]
		
		for p in players:
			#print self.my_position.distance(self.state.player_state(p[0], p[1]).position)
			#print self.my_position.distance(self.state.player_state(pp[0], pp[1]).position)
			if self.my_position.distance(self.state.player_state(p[0], p[1]).position) < self.my_position.distance(self.state.player_state(pp[0], pp[1]).position):
				pp = p
		return pp
	
	#true if player p near ball
	def p_near_ball(self, p):
		return True if self.ball_position.distance(self.state.player_state(p[0], p[1]).position) < 20 else False
		
	
	def joueur_pos(self, x, y) :
		for p in self.all_players :
			if ( self.state.player_state(p[0], p[1]).position == Vector2D(x, y) ) :
				return p
				
	def drible(self) :
		adv = self.adv_nearby()
		sens = 1
		if adv[0] == 2 :
			sens = 1
		else:
			sens = -1
		
		me = self.my_position
		adv_pos = self.state.player_state(adv[0], adv[1]).position
		#print self.state.player_state(self.key[0], self.key[1])._rd_angle(Vector2D(1, 1), 90, 1)
		if sens == 1 :
			if me.x < adv_pos.x :
				if me.y < adv_pos.y :
					return self.shoot(self.ball_position + sens*Vector2D(10, -10)) + self.aller(self.ball_position + sens*Vector2D(10, -10))
				else :
					return self.shoot(self.ball_position+ sens*Vector2D(10, 10)) + self.aller(self.ball_position + sens*Vector2D(10, -10))
			else :
				return self.shoot((self.but_adv+me)/2)
		else :
			if me.x > adv_pos.x :
				if me.y	< adv_pos.y :
					return self.shoot(self.ball_position + sens*Vector2D(10, 10)) + self.aller(self.ball_position + sens*Vector2D(10, -10))	
				else:
					return self.shoot(self.ball_position+ sens*Vector2D(10, -10)) + self.aller(self.ball_position + sens*Vector2D(10, -10))
			else :
				return self.shoot((self.but_adv+me)/2)
						











