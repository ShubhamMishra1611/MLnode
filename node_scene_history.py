from node_graphics_edge import Qgraphics_edge
from pprint import pprint

DEBUG = False

class scene_history:
    def __init__(self, scene) -> None:
        self.scene = scene
        self.history_stack = []
        self.history_stack_max_length = 16
        self._history_modified_listeners = []
        self.history_current_idx = -1

    def undo(self):
        if DEBUG: print("UNDO")
        if self.canUndo():
            self.history_current_idx -= 1
            self.restore_history()
            self.scene._has_been_modified = True
    
    def clear(self):
        self.history_stack = []
        self.history_current_idx = -1

    
    def redo(self):
        if DEBUG: print("REDO")
        if self.canRedo():
            self.history_current_idx+=1
            self.restore_history()
            self.scene._has_been_modified = True

    def addHistoryModifiedListener(self, callback):
        self._history_modified_listeners.append(callback)


    def restore_history(self):
        if DEBUG: print(f"restoring history ... current step : {self.history_current_idx} and length is : {len(self.history_stack)}")
        self.restore_history_stamp(self.history_stack[self.history_current_idx])
        for callback in self._history_modified_listeners: callback()

    def store_history(self, desc):
        if DEBUG: print(f'storing history with current step: {self.history_current_idx} and length is : {len(self.history_stack)}')
        
        if self.history_current_idx+1 < len(self.history_stack):
            self.history_stack = self.history_stack[0:self.history_current_idx+1]
        
        if self.history_current_idx+1 >= self.history_stack_max_length:
            self.history_stack = self.history_stack[1:]
            self.history_current_idx-=1
        
        hs = self.create_history_stamp(desc)
        self.history_stack.append(hs)
        self.history_current_idx+=1
        for callback in self._history_modified_listeners: callback()

    def create_history_stamp(self, desc):
        sel_obj = {
            'nodes': [],
            'edges':[]
        }

        for item in self.scene.grscene.selectedItems():
            if hasattr(item, 'node'):
                sel_obj['nodes'].append(item.node.id)
            if isinstance(item, Qgraphics_edge):
                sel_obj['edges'].append(item.edge.id)
        history_stamp = {
            'desc': desc,
            'snapshot': self.scene.serialize(),
            'selection': sel_obj
        }
        pprint(history_stamp)
        return history_stamp
    
    def storeInitialHistoryStamp(self):
        self.store_history("Initial History Stamp")

    def canUndo(self):
        return self.history_current_idx > 0

    def canRedo(self):
        return self.history_current_idx + 1 < len(self.history_stack)

    
    def restore_history_stamp(self, history_stamp):
        if DEBUG: print(f'RHS: ', history_stamp)

        try:
            self.scene.deserialize(history_stamp['snapshot'])

            # restore selection
            for edge_id in history_stamp['selection']['edges']:
                for edge in self.scene.edges:
                    if edge.id == edge_id:
                        edge.graphical_edge.setSelected(True)
                        break
            for node_id in history_stamp['selection']['nodes']:
                for node in self.scene.nodes:
                    if node.id == node_id:
                        node.graphical_node.setSelected(True)
                        break

        except Exception as e:
            from utility import print_traceback
            print_traceback(e)
            print("Error restoring history stamp", e)
            return False