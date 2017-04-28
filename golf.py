from soccersimulator import GolfState,Golf,Parcours1,Parcours2,Parcours3,Parcours4
from soccersimulator import SoccerTeam,show_simu
from soccersimulator import Strategy,SoccerAction,Vector2D,settings
import math
GOLF = 0.001
SLALOM = 10.


class DemoStrategy(Strategy):
    def __init__(self):
        super(DemoStrategy,self).__init__("Demo")
    def compute_strategy(self,state,id_team,id_player):
        """ zones : liste des zones restantes a valider """
        zones = state.get_zones(id_team)
        me = state.player_state(id_team, id_player).position 
        if len(zones)==0:
            """ shooter au but """
            return SoccerAction(state.ball.position-state.player_state(id_team,id_player).position,\
                    Vector2D((2-id_team)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)-state.ball.position)
        """ zone : carre de zone avec z.position angle bas,gauche et z.l longueur du cote
            centre du carre : zone.position+Vector2D(z.l/2.,z.l/2.)
            zone.dedans(point) : teste si le point est dans la zone
        """
        zone = zones[0]
        """ si la ball est dans une zone a valider """
        if zone.dedans(state.ball.position):
            return SoccerAction()
        """ sinon """
        distance = state.player_state(id_team,id_player).position.distance(zone.position+Vector2D(zone.l,zone.l))
        return SoccerAction()

class Golf(Strategy):
    def __init__(self):
        super(Golf,self).__init__("Golf")
		
    def compute_strategy(self,state,id_team,id_player):
        """ zones : liste des zones restantes a valider """
        zones = state.get_zones(id_team)
        my_pos = state.player_state(id_team, id_player).position 
        ball = state.ball
       	but = Vector2D(150, 45) if id_team == 1 else Vector2D(0, 45)	
        if len(zones)==0:
            """ shooter au but """
            return SoccerAction(ball.position - my_pos,\
                    Vector2D((2-id_team)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)-ball.position)
        """ zone : carre de zone avec z.position angle bas,gauche et z.l longueur du cote
            centre du carre : zone.position+Vector2D(z.l/2.,z.l/2.)
            zone.dedans(point) : teste si le point est dans la zone
        """
        zone = zones[0]
        
        """ si la ball est dans une zone a valider je vais vers la balle"""
        if zone.dedans(ball.position):
            return SoccerAction()#SoccerAction(Vector2D(), but - my_pos)
       
        """ sinon """
        d_ball = my_pos.distance(ball.position) #distance de la balle
        distance = my_pos.distance(zone.position+Vector2D(zone.l/2.,zone.l/2.)) #distance de la zone
        
        if d_ball > 1:
        	return SoccerAction(((d_ball/4)%20)*(ball.position - my_pos), Vector2D()) #aller vers la balle
        
        if distance > 35:
        	return SoccerAction(Vector2D(), (zone.position + Vector2D(zone.l/2.,zone.l/2.) - my_pos)/(distance/2)) #tirer dans la zone
        
        if distance < 35 and distance > zone.l/2 :
        	return SoccerAction(Vector2D(), (zone.position + Vector2D(zone.l/2.,zone.l/2.)- my_pos)/(2*distance)) #tirer dans la zone
   
class Slalom(Strategy):
	def __init__(self):
		super(Slalom,self).__init__("Slalom")

	def compute_strategy(self,state,id_team,id_player):
		""" zones : liste des zones restantes a valider """
		zones = state.get_zones(id_team)
		my_pos = state.player_state(id_team, id_player).position 
		ball = state.ball
		but = Vector2D(150, 45) if id_team == 1 else Vector2D(0, 45)	
		if len(zones)==0:
			""" shooter au but """
			return SoccerAction(ball.position - my_pos, Vector2D((2-id_team)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)-ball.position)

		zone = zones[0]

		if zone.dedans(ball.position):
			return SoccerAction()#SoccerAction(Vector2D(), but - my_pos)

		d_ball = my_pos.distance(ball.position) #distance de la balle
		distance = my_pos.distance(zone.position+Vector2D(zone.l/2.,zone.l/2.)) #distance de la zone

		if d_ball > 1:
			return SoccerAction(((d_ball/4)%20)*(ball.position - my_pos), Vector2D()) #aller vers la balle
		if distance > 35:
			return SoccerAction(Vector2D(), (zone.position + Vector2D(zone.l/2.,zone.l/2.) - my_pos)/(distance/2)) #tirer dans la zone

		if distance < 35 and distance > 10 :
			return SoccerAction(Vector2D(), (zone.position + Vector2D(zone.l/2.,zone.l/2.)- my_pos)/(distance)) #tirer dans la zone
		#return SoccerAction(Vector2D(), (zone.position + Vector2D(zone.l/2.,zone.l/2.)- my_pos)/(2*distance))
				
team1 = SoccerTeam()
team2 = SoccerTeam()
team3 = SoccerTeam()
team1.add("Solo",Golf())
team2.add("John",Slalom())
team3.add("michemiche", DemoStrategy())

simu = Parcours1(team1=team1,vitesse=GOLF)
show_simu(simu)
simu = Parcours2(team1=team1,vitesse=GOLF)
show_simu(simu)

simu = Parcours3(team1=team2,vitesse=SLALOM)
show_simu(simu)

simu = Parcours4(team1=team3,team2=team2,vitesse=SLALOM)
show_simu(simu)
