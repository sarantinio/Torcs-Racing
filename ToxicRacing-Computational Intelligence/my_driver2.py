from pytocl.driver import Driver
from pytocl.car import State, Command,MPS_PER_KMH
import numpy as np
from keras.models import model_from_json
import keras

from pytocl.main import main
from pytocl.controller import CompositeController, ProportionalController, \
	IntegrationController, DerivativeController

# loaded_model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
import logging

from pytocl.analysis import DataLogWriter
class MyDriver(Driver):
    # Override the `drive` method to create your own driver
	
	def __init__(self,log_data=False, net=None):
		# self.steering_ctrl = CompositeController(ProportionalController(0.4),IntegrationController(0.2, integral_limit=1.5),DerivativeController(2))
		# self.acceleration_ctrl = CompositeController(
		# 	ProportionalController(3.7),
		# )
		# json_file = open('model.json', 'r')
		# loaded_model_json = json_file.read()
		# json_file.close()
		# loaded_model = model_from_json(loaded_model_json)
		# loaded_model.compile(loss='mean_squared_error', optimizer='rmsprop', metrics=['accuracy'])
		# # load weights into new model
		# self.loaded_model=loaded_model.load_weights("model.h5")
		# print("Loaded model from disk")
		# self.steering_ctrl = CompositeController(
		# 	ProportionalController(0.4),
		# 	DerivativeController(1)
		# )
		# self.acceleration_ctrl = CompositeController(
		# 	ProportionalController(3.7),
		# )
		self.data_logger = DataLogWriter() if log_data else None
		self.net=net
		print("mehmehmeh")
		self.flag=False
	def drive(self, carstate: State):
		X=np.zeros((1,41))
		# # print("mehmeh",carstate)
		# # X[0]=carstate.speed
		with open('model.json', 'r') as json_file:
			loaded_model_json = json_file.read()
		json_file.close()	
		loaded_model = model_from_json(loaded_model_json)
		# load weights into new model
		loaded_model.load_weights("model.h5")
		print("Loaded model from disk")
		X[0][0]=carstate.angle

		print('meh')




		X[0][1]=carstate.speed_x/280

		# X[3]=carstate.distance_from_start
		X[0][21]=carstate.distances_from_edge[0]/200
		X[0][22]=carstate.distances_from_edge[1]/200
		X[0][23]=carstate.distances_from_edge[2]/200
		X[0][24]=carstate.distances_from_edge[3]/200
		X[0][25]=carstate.distances_from_edge[4]/200
		X[0][26]=carstate.distances_from_edge[5]/200
		X[0][27]=carstate.distances_from_edge[6]/200
		X[0][28]=carstate.distances_from_edge[7]/200
		X[0][29]=carstate.distances_from_edge[8]/200
		X[0][30]=carstate.distances_from_edge[9]/200
		X[0][31]=carstate.distances_from_edge[10]/200

		X[0][32]=carstate.distances_from_edge[11]/200

		X[0][33]=carstate.distances_from_edge[12]/200

		X[0][34]=carstate.distances_from_edge[13]/200

		X[0][35]=carstate.distances_from_edge[14]/200

		X[0][36]=carstate.distances_from_edge[15]/200

		X[0][37]=carstate.distances_from_edge[16]/200

		X[0][38]=carstate.distances_from_edge[17]/200

		X[0][39]=carstate.distances_from_edge[18]/200

		# print(carstate.distances_from_edge[19])
		X[0][40]=carstate.distance_from_center
		X[0][2]= carstate.opponents[0]/200
		X[0][3]= carstate.opponents[1]/200
		X[0][4]=carstate.opponents[2]/200
		X[0][5]=  carstate.opponents[3]/200
		X[0][6]=carstate.opponents[4]/200
		X[0][7]= carstate.opponents[5]/200
		X[0][8]= carstate.opponents[6]/200
		X[0][9]= carstate.opponents[7]/200
		X[0][10]= carstate.opponents[8]/200
		X[0][11]= carstate.opponents[9]/200
		X[0][12]= carstate.opponents[10]/200
		X[0][13]=carstate.opponents[11]/200
		X[0][14]= carstate.opponents[12]/200
		X[0][15]= carstate.opponents[13]/200
		X[0][16]= carstate.opponents[14]/200
		X[0][17]= carstate.opponents[15]/200
		X[0][18]= carstate.opponents[16]/200
		X[0][19]=  carstate.opponents[17]/200
		X[0][20]= carstate.opponents[19]/200
		# fitnesses = []
		sumofSensors=0
		for i in range(19):
			sumofSensors+=np.sqrt(carstate.distances_from_edge[i])

		# print((summ*0.3)+50)
		#action = self.net.advance(X, 1, 10)
		print('mehblahmeh')
#-------------------------------------------------------------------------------
		action=loaded_model.predict(X,batch_size=1,verbose=1)
		print('mehblahmeh',action)
		# exit()
 







#-------------------------------------------------------------------------------
		# front=((carstate.distances_from_edge[8]+carstate.distances_from_edge[9])/2)
		# brakeoff=0
		# if front<100 :
		# 	manualSpeed=70
		# 	if not self.flag:
		# 		brakeOff=0.50
		# 		self.flag=True
		# 	else:
		# 		brakeOff=0
			
		# else:
		# 	self.flag=False
		# 	brakeOff=0
		# 	manualSpeed=front+50
		# # print(front)
		# # print(action)
		# # print("heeeey")
		# summ=np.zeros(6)
		# for i in range(len(X[4:])):
		# 	# print(len(X[4:]))
		# 	if i <4 :
		# 		summ[0]+=X[i]
		# 	elif i<7:
		# 		summ[1]+=X[i]
		# 	elif i<9:
		# 		summ[2]+=X[i]
		# 	elif i<11:
		# 		summ[3]+=X[i]
		# 	elif i<14:
		# 		summ[4]+=X[i]
		# 	elif i<18:
		# 		summ[5]+=X[i]


		command = Command()
		# if carstate.gear ==3:
		# 	gear=3
		# v_x= (action[0]*170)+40#(sumofSensors*1.3)#((action[2]*250)**2)+70

		# self.accelerate(carstate, v_x, command)

		# print(command.accelerator)
		# averages=np.zeros(10)
		# averages[0]=summ[0]/4
		# averages[1]=summ[1]/3*5
		# averages[2]=summ[2]/2*15
		# averages[3]=summ[3]/2*15
		# averages[4]=summ[4]/3*5
		# averages[5]=summ[5]/4
		# averages[6]=X[0]
		# averages[7]=X[1]
		# averages[8]=X[2]
		# averages[9]=command.accelerator
		gear=carstate.gear 
		# X[0]=carstate.
		# X[0]=carstate.speed
# gear=carstate.gear
		# inp=np.zeros(3)
		# inp[0]=command.accelerator
		# inp[1]=X[1]
		# inp[2]=X[2]
		# # X[0]=carstate.
		# X[0]=carstate.speed

		Kp=0.003
		dfromC=carstate.distance_from_center
		# if carstate.distance_from_center==-1:
		# 	dfromC=-10
		# elif carstate.distance_from_center==1:
		# 	dfromC=10
		error=(carstate.angle-dfromC*12)
		pidoff=Kp*carstate.angle*100
		pid=Kp*error
		# print(action)
		# print(pid)
		# X=list(carstate)
		# print(X)
		#self.net.Input(X)
		#self.net.Activate()
		#action = self.net.Output()
	
		# # print(action,"mehblah")
		
		# # # if y[0][0] > 0:
		# ((action[0]*2)-1)*0.7
		# x=np.array(())
		# self.steer(carstate,0, command)
  #       # else:
  #       #     command.brake = min(-acceleration, 1)
		# steer=action[0]
		# if (action[0]*2)-1<-0.2:
		# 	steer=-0.2
		# elif (action[0])*2-1>0.2:
		# 	steer=0.2
		# brake=0.01
		# if action[1]>0.8:
		# 	accel=0.8
		# elif action[1]<0.4:
		# 	accel=0.4
		# steeraction=action.index(max(action))
		# if steeraction==0:
		# 	command.steering=-0.7
		# elif steeraction==1:
		# 	command.steering=-0.4
		# elif steeraction==2:
		# 	command.steering=-0.2
		# elif steeraction==3:
		# 	command.steering=-0.1
		# elif steeraction==4:
		# 	command.steering=-0.05
		# elif steeraction==5:
		# 	command.steering=0
		# elif steeraction==6:
		# 	command.steering=0.05
		# elif steeraction==7:
		# 	command.steering=0.1
		# elif steeraction==8:
		# 	command.steering=0.2
		# elif steeraction==9:
		# 	command.steering=0.4
		# elif steeraction==10:
		# 	command.steering=0.7

		# brake=action[2]
		# if action[2]>0.2:
		# 	brake=0.2
		# elif action[1]<0.4:
		# 	accel=0.4

		# v_x = (((((action[2]-1)*-1)**2)-1)*-1*100)+95

		# if carstate.rpm < 2500:
		# 	command.gear = carstate.gear - 1

		# if not command.gear:
		# 	command.gear = 1
		# print("mehblah",carstate.distance_from_center)
		# self.data_logger.log(carstate,command)
		# print(y)
		# if carstate.distance_from_center>1.5 or carstate.distance_from_center<-1.5:

		# 	self.data_logger.close()
		# 	self.data_logger = None
		# else:

				# if carstate.distances_from_edge[8]<65 and carstate.distances_from_edge[8]>0:
		# 	command.brake=(((carstate.distances_from_edge[8]/65)-1)*-1)**3
		# # if carstate.distances_from_edge[8]==-1.0:
		# 	command.brake=0
		# 	command.accelerator=0.8
		# 	command.steering=pidoff
		# print(action)
		# print((action[0]*2)-1)
		if carstate.rpm>7000:
			gear+=1
		elif carstate.gear==0:
			gear+=1
		elif carstate.rpm<2000 and X[0][1]>10:
		 	print(X[0][1])
		 	gear-=1
		# if command.accelerator==0:
		# 	command.brake=0.02
		# else:
		# 	command.brake=0
		print('blahandreas',action[0][0])
		command.accelerator=1#float(action[0][0])+2#0.4#accel#y[0][0]
		command.brake=action[0][1]#abs(pid)*2#y[0][1]*y[0][1]
		command.steering=action[0][2]
		# command.steering=((action[0]*2)-1)*0.7#steer
		command.gear=gear
		command.focus=0
		# command.gear=1
		# print(command)
		# print(command)
		return command
