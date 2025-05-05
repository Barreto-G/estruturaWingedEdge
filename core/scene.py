from .winged_edge import WingedEdge

class Scene:
    """
    Suporta múltiplos objetos WingedEdge em uma cena.
    """
    def __init__(self):
        self._objects: dict[int, WingedEdge] = {}
        self._next_id = 1
        self._selected_id = None

    @property
    def objects(self):
        return self._objects.copy()

    @property
    def selected_object(self):
        return self._objects.get(self._selected_id)

    @property
    def selected_id(self):
        return self._selected_id

    def add_object(self, winged_edge: WingedEdge):
        """
        Adiciona um objeto à cena e retorna seu ID.
        """
        if not isinstance(winged_edge, WingedEdge):
            raise TypeError("O objeto deve ser uma instância de WingedEdge")

        object_id = self._next_id
        self._objects[object_id] = winged_edge
        self._next_id += 1
        return object_id

    def remove_object(self, object_id):
        """
        Remove um objeto da cena pelo ID.
        Retorna True se o objeto foi removido, False caso contrário.
        """
        if object_id in self._objects:
            del self._objects[object_id]
            if self._selected_id == object_id:
                self._selected_id = None
            return True
        return False

    def get_object(self, object_id):
        return self._objects.get(object_id)

    def select_object(self, object_id):
        """
        Seleciona um objeto na cena.
        Retorna True se a seleção foi bem sucedida, False caso contrário.
        """
        if object_id is None or object_id in self._objects:
            self._selected_id = object_id
            return True
        return False

    def clear(self):
        """Remove todos os objetos da cena."""
        self._objects.clear()
        self._selected_id = None
        self._next_id = 1

    def get_object_info(self, object_id):
        """
        Retorna informações sobre um objeto específico.
        """
        obj = self._objects.get(object_id)
        if not obj:
            return None

        return {
            'id': object_id,
            'vertices': obj.vertex_count,
            'edges': obj.edge_count,
            'faces': obj.face_count,
            'centroid': obj.centroid.copy(),
            'selected': object_id == self._selected_id
        }

    def __len__(self):
        """Retorna o número de objetos na cena."""
        return len(self._objects)

    def __bool__(self):
        """Se a cena contém objetos."""
        return bool(self._objects)