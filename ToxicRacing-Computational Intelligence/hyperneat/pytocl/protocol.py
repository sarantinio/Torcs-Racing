import enum
import logging
import socket

from pytocl.car import State as CarState
from pytocl.driver import Driver
import numpy as np
_logger = logging.getLogger(__name__)

# special messages from server:
MSG_IDENTIFIED = b'***identified***'
MSG_SHUTDOWN = b'***shutdown***'
MSG_RESTART = b'***restart***'

# timeout for socket connection in seconds and msec:
TO_SOCKET_SEC = 1
TO_SOCKET_MSEC = TO_SOCKET_SEC * 1000


class Client:
    """Client for TORCS racing car simulation with SCRC network server.

    Attributes:
        hostaddr (tuple): Tuple of hostname and port.
        port (int): Port number to connect, from 3001 to 3010 for ten clients.
        driver (Driver): Driving logic implementation.
        serializer (Serializer): Implementation of network data encoding.
        state (State): Runtime state of the client.
        socket (socket): UDP socket to server.
    """

    def __init__(self, hostname='localhost', port=3001, *,
                 driver=None, serializer=None,data=None):
        self.hostaddr = (hostname, port)
        self.driver = driver or Driver()
        self.serializer = serializer or Serializer()
        self.state = State.STOPPED
        self.socket = None
        self.datafile=data
        _logger.debug('Initializing {}.'.format(self))
        self.crashed=False
        self.stuck=False
        self.fitness=0
        self.timespend=0
        self.stack=0
        self.count=0
        self.sumspeed=0
        self.speed=0
        self.position=0
        self.speedReward=0
        self.positionReward=0
        self.notTurnFlag=True
        self.roadError=0
    def __repr__(self):
        return '{s.__class__.__name__}({s.hostaddr!r}) -- {s.state.name}' \
            ''.format(s=self)

    def run(self):
        """Enters cyclic execution of the client network interface."""

        if self.state is State.STOPPED:
            _logger.debug('Starting cyclic execution.')

            self.state = State.STARTING

            try:
                # _logger.info('Registering driver client with server {}.'
                             # .format(self.hostaddr))
                self._configure_udp_socket()
                self._register_driver()
                self.state = State.RUNNING
                # _logger.info('Connection successful.')

            except socket.error as ex:
                # _logger.error('Cannot connect to server: {}'.format(ex))
                self.state = State.STOPPED

        while self.state is State.RUNNING:
            self._process_server_msg()


        # _logger.info('Client stopped.')
        self.state = State.STOPPED

    def stop(self):
        """Exits cyclic client execution (asynchronously)."""
        if self.state is State.RUNNING:
            # _logger.info('Disconnecting from racing server.')
            self.state = State.STOPPING
            self.driver.on_shutdown()

    def _configure_udp_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(TO_SOCKET_SEC)

    def _register_driver(self):
        """
        Sends driver's initialization data to server and waits for acceptance
        response.
        """

        angles = self.driver.range_finder_angles
        assert len(angles) == 19, \
            'Inconsistent length {} of range of finder iterable.'.format(
                len(angles)
            )

        data = {'init': angles}
        buffer = self.serializer.encode(
            data,
            prefix='SCR-{}'.format(self.hostaddr[1])
        )

        # _logger.info('Registering client.')

        connected = False
        while not connected and self.state is not State.STOPPING:
            try:
                _logger.debug('Sending init buffer {!r}.'.format(buffer))
                self.socket.sendto(buffer, self.hostaddr)

                buffer, _ = self.socket.recvfrom(TO_SOCKET_MSEC)
                _logger.debug('Received buffer {!r}.'.format(buffer))
                if MSG_IDENTIFIED in buffer:
                    _logger.debug('Server accepted connection.')
                    connected = True

            except socket.error as ex:
                _logger.debug('No connection to server yet ({}).'.format(ex))

    def _process_server_msg(self):
        
        try:
            buffer, _ = self.socket.recvfrom(TO_SOCKET_MSEC)
            _logger.debug('Received buffer {!r}.'.format(buffer))

            if not buffer:
                return

            elif MSG_SHUTDOWN in buffer:
                _logger.info('Server requested shutdown.')
                # if self.position==1:
                #     meh=1000
                # if self.position==2:
                #     meh=500
                # if self.position==3:
                #     meh=200
                # if self.position==4:
                #     meh=100
                with open(self.datafile,'w') as f:
                    fitt=str(self.fitness+15)
                    f.write(fitt)
                    

                    self.stop()

            elif MSG_RESTART in buffer:

                _logger.info('Server requested restart of driver.')
                self.driver.on_restart()

            else:

                sensor_dict = self.serializer.decode(buffer)
                carstate = CarState(sensor_dict)
                command = self.driver.drive(carstate)
                _logger.debug(carstate)
                # print(carstate)
                if command.steering!=-0.7 :
                    #print("blah")
                    self.notTurnFlag=False
                if carstate.current_lap_time>5:
                   
                    if carstate.distance_from_center<-1.2 or carstate.distance_from_center>1.2:
                        self.crashed=True
                    if   (carstate.speed_x<2 and carstate.current_lap_time>6  ):
                        self.stuck=True
                
                # if carstate.distance_raced%22784==0:
                #     self.stack+=carstate.last_lap_time
                self.timespend=carstate.current_lap_time#+self.stack

                # self.fitness=carstate.distance_raced -carstate.current_lap_time*10
                if self.crashed :
                    
                    with open(self.datafile,'w') as f:

                        fitt=str(self.fitness-10)
                        f.write(fitt)
                        self.stop()
                elif self.stuck:
                    with open(self.datafile,'w') as f:

                        fitt=str(self.fitness  - 15) 
                        f.write(fitt)
                
                        self.stop()
                else:
                    self.count+=1
                    self.sumspeed+=carstate.speed_x
                    self.speed=self.sumspeed/self.count

                    #self.roadError+=abs(carstate.distance_from_center)


                    # print(carstate.race_position)
                    # if carstate.speed_x<80:
                    #     self.speedReward-=0.01
                    # elif carstate.speed_x<110:
                    #     self.speedReward+=0.01
                    # else:
                    #     self.speedReward+=0.02
                    self.position=carstate.race_position
                    # if carstate.distance_raced>200:
                    # if self.position==1:
                    #     self.positionReward+=0.1
                    # if self.position==2:
                    #     self.positionReward+=0.5
                    #     if self.position==3:
                    #         self.positionReward+=0.2
                        # if self.position==4:
                        #     self.positionReward+=0.1
                    
                    if not self.notTurnFlag:
                        if carstate.distance_raced>400:
                            self.fitness=float((self.speed+float(carstate.distance_raced /100)) + self.positionReward+self.speedReward) +30 -self.roadError 
                # return "andreas is meh ********************************"
                        else:
                            self.fitness=float(self.speed+float(carstate.distance_raced /100))+ self.positionReward+self.speedReward -self.roadError
                    else:
                        self.fitness=0



              
                # print("this is the message",sensor_dict)

                _logger.debug(command)
                buffer = self.serializer.encode(command.actuator_dict)
                _logger.debug('Sending buffer {!r}.'.format(buffer))
                self.socket.sendto(buffer, self.hostaddr)

        except socket.error as ex:
            _logger.warning('Communication with server failed: {}.'.format(ex))

        except KeyboardInterrupt:
            _logger.info('User requested shutdown.')
            self.stop()


class State(enum.Enum):
    """The runtime state of the racing client."""

    # not connected to a racing server
    STOPPED = 1,
    # entering cyclic execution
    STARTING = 2,
    # connected to racing server and evaluating driver logic
    RUNNING = 3,
    # exiting cyclic execution loop
    STOPPING = 4,


class Serializer:
    """Serializer for racing data dirctionary."""

    @staticmethod
    def encode(data, *, prefix=None):
        """Encodes data in given dictionary.

        Args:
            data (dict): Dictionary of payload to encode. Values are arrays of
                numbers.
            prefix (str|None): Optional prefix string.

        Returns:
            Bytes to be sent over the wire.
        """

        elements = []

        if prefix:
            elements.append(prefix)

        for k, v in data.items():
            if v and v[0] is not None:
                # string version of number array:
                vstr = map(lambda i: str(i), v)

                elements.append('({} {})'.format(k, ' '.join(vstr)))

        return ''.join(elements).encode()

    @staticmethod
    def decode(buff):
        """
        Decodes network representation of sensor data received from racing
        server.
        """
        d = {}
        s = buff.decode()

        pos = 0
        while len(s) > pos:
            start = s.find('(', pos)
            if start < 0:
                # end of list:
                break

            end = s.find(')', start + 1)
            if end < 0:
                _logger.warning('Opening brace at position {} not matched in '
                                'buffer {!r}.'.format(start, buff))
                break

            items = s[start + 1:end].split(' ')
            if len(items) < 2:
                _logger.warning(
                    'Buffer {!r} not holding proper key value pair.'.format(
                        buff
                    )
                )
            else:
                key = items[0]
                if len(items) == 2:
                    value = items[1]
                else:
                    value = items[1:]
                d[key] = value

            pos = end + 1

        return d
