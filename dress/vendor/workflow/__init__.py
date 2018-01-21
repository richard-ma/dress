__all__ = ['Action', 'DebugAction', 'Workflow']

import queue


class Action(object):
    def __init__(self, **kwargs):
        self.params = kwargs

    def run(self, *data):
        return None


class DebugAction(object):
    def run(self, *data):
        print("\n".join(data[0]))
        return False


class Workflow(object):
    def __init__(self, initData=None):
        self.actions = queue.Queue()
        self.initData = initData

    def push(self, action: Action):
        self.actions.put(action)
        return self

    def execute(self):
        data = self.initData
        while self.actions.qsize() > 0:
            action = self.actions.get()
            data = action.run(data)
            # Break processing of workflow when previous action data is False
            if data == False:
                return False
        return True


# Usage
#
#if __name__ == "__main__":
#Workflow(list()
#).push(Action(hello='world')
#).push(Action(buy='buy buy')
#).execute()
