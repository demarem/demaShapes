import eventManager
import keyboardContoller
import timeController
import runController
import pygameView
import game

def main():
    eventMgr = eventManager.EventManager()

    keyboard = keyboardContoller.KeyboardController(eventMgr)
    runner = runController.RunController(eventMgr)
    timer = timeController.TimeController(eventMgr)

    view = pygameView.PygameView(eventMgr)

    currentGame = game.Game(eventMgr)

    runner.run()

if __name__ == '__main__':
    main()
