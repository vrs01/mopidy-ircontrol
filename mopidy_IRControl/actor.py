import pykka
import pylirc
import logging
import tempfile

from time import sleep

from mopidy.core import PlaybackState
from mopidy.utils import process

logger = logging.getLogger('mopidy_IRControl')

LIRC_PROG_NAME = "mopidyIRControl"


class CommandDispatcher(object):
    def __init__(self, core):
        self.core = core
        self._handlers = {}
        self.registerHandler('playpause', self._playpauseHandler)
        self.registerHandler('mute', self._muteHandler)
        self.registerHandler('stop', lambda: self.core.playback.stop().get())
        self.registerHandler('next', lambda: self.core.playback.next().get())
        self.registerHandler('previous',
                             lambda: self.core.playback.previous().get())
        self.registerHandler('volumedown',
                             self._volumeFunction(lambda vol: vol - 5))
        self.registerHandler('volumeup',
                             self._volumeFunction(lambda vol: vol + 5))

    def handleCommand(self, cmd):
        if cmd in self._handlers:
            self._handlers[cmd]()
        else:
            logger.info("Command {0} was not handled".format(cmd))

    def registerHandler(self, cmd, handler):
        self._handlers[cmd] = handler

    def _playpauseHandler(self):
        state = self.core.playback.state.get()
        if(state == PlaybackState.PAUSED):
            self.core.playback.resume().get()
        elif (state == PlaybackState.PLAYING):
            self.core.playback.pause().get()
        elif (state == PlaybackState.STOPPED):
            self.core.playback.play().get()

    def _muteHandler(self):
        self.core.playback.mute = not self.core.playback.mute.get()

    def _volumeFunction(self, changeFct):
        def volumeChange():
            vol = self.core.playback.volume.get()
            self.core.playback.volume = min(max(0, changeFct(vol)), 100)
        return volumeChange


class LircThread(process.BaseThread):
    def __init__(self, core, configFile):
        super(LircThread, self).__init__()
        self.name = 'Lirc worker thread'
        self.core = core
        self.configFile = configFile
        self.dispatcher = CommandDispatcher(core)
        self.frontendActive = True

    def run_inside_try(self):
        self.startPyLirc()

    def startPyLirc(self):
        if(pylirc.init(LIRC_PROG_NAME, self.configFile, 0)):
            while(self.frontendActive):
                s = pylirc.nextcode(1)
                self.handleNextCode(s)
                sleep(0.1)
            pylirc.exit()

    def handleNextCode(self, s):
        if s:
            self.handleLircCode(s)

    def handleLircCode(self, s):
        for code in s:
            self.handleCommand(code['config'])

    def handleCommand(self, cmd):
        logger.debug('Command: {0}'.format(cmd))
        self.dispatcher.handleCommand(cmd)


class IRControlFrontend(pykka.ThreadingActor):
    def __init__(self, config, core):
        super(IRControlFrontend, self).__init__()
        self.core = core
        self.configFile = self.generateLircConfigFile(config['IRControl'])
        logger.debug('lircrc file:{0}'.format(self.configFile))

    def on_start(self):
        try:
            logger.debug('IRControl starting')
            self.thread = LircThread(self.core, self.configFile)
            self.thread.start()
            logger.debug('IRControl started')
        except Exception:
            logger.warning('IRControl has not started')
            self.stop()

    def on_stop(self):
        logger.info('IRControl stopped')
        self.thread.frontenActive = False
        self.thread.join()

    def on_failure(self):
        logger.warning('IRControl failing')
        self.thread.frontenActive = False
        self.thread.join()

    def generateLircConfigFile(self, config):
        '''Returns file name of generate config file for pylirc'''
        f = tempfile.NamedTemporaryFile(delete=False)
        skeleton = 'begin\n   prog={2}\n   button={0}\n   config={1}\nend\n'
        for action in config:
            entry = skeleton.format(config[action], action, LIRC_PROG_NAME)
            f.write(entry)
        f.close()
        return f.name
