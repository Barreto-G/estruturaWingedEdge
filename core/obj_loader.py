from .scene import Scene
from .winged_edge import WingedEdge

def read_obj(filename):
    """Lê um arquivo .obj e retorna um objeto da classe Scene."""
    scene = Scene()
    mesh = WingedEdge()
    edge_map = {}
    
    try:
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if not parts:
                    continue
                    
                if parts[0] == 'v':
                    coords = [float(coord) for coord in parts[1:4]]
                    vertex_id = len(mesh.vertices) + 1
                    mesh.add_vertex(vertex_id, coords)
                    
                elif parts[0] == 'f':
                    vertex_indices = []
                    for part in parts[1:]:
                        vertex_index = int(part.split('/')[0])
                        vertex_indices.append(vertex_index)

                    edge_ids = []
                    for i in range(len(vertex_indices)):
                        v1 = vertex_indices[i]
                        v2 = vertex_indices[(i + 1) % len(vertex_indices)]
                        
                        edge_key = tuple(sorted([v1, v2]))
                        
                        if edge_key not in edge_map:
                            edge_id = len(mesh.edges) + 1
                            mesh.add_edge(edge_id, v1, v2)
                            edge_map[edge_key] = edge_id
                        
                        edge_ids.append(edge_map[edge_key])

                    # Adiciona a face, mantendo a ordem original dos vertices
                    face_id = len(mesh.faces) + 1
                    mesh.add_face(face_id, edge_ids, vertex_indices)

        mesh.link_edges()
        mesh.calculate_centroid()
        scene.add_object(mesh)
        
        return scene

    except Exception as e:
        raise ValueError(f"Erro ao processar o arquivo: {str(e)}")