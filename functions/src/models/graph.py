"""Model representing the level as a graph data structure."""

import random
from typing import Type

from src import exceptions
from src.models.entity import Entity
from src.models.environment import Gate, Teleporter
from src.models.node import Node
from src.models.path import Path
from src.models.pickups import Pickup
from src.models.position import Position


class Graph:
    """Model representing the level as a graph data structure."""

    def __init__(self) -> None:
        """
        Initialises the Graph.
        """
        self.level: dict[Node, list[Node]] = {}
        """
        The level represented as a graph.

        This is represented in this case as an adjacency list allowing relations
        to be mapped between nodes and their direct adjacents.
        """
        self.node_count = 1
        """The counter used to identify nodes."""
        self.total_pickups: int
        """The total number of pickups contained in this level."""

    def __repr__(self) -> str:
        string = ""
        for parent, children in self.level.items():
            string += f"{parent.position}: {[child.position for child in children]}\n"
        return string

    def num_of_nodes(self) -> int:
        """
        Returns the size of the graph.

        Returns
        -------
        The number of nodes within the graph.
        """
        return len(self.level.keys())

    def num_of_edges(self) -> int:
        """
        Returns the number of edges within the graph.

        Returns
        -------
        The number of edges within the graph
        """
        counter = 0
        for connections in self.level.values():
            counter += len(connections)
        return counter

    def nodes(self) -> list[Node]:
        """
        Returns all of the nodes in the graph.

        Returns
        -------
        A list containing all of the nodes present in the graph.
        """
        return list(self.level.keys())

    def add_node(self, node: Node) -> None:
        """
        Adds a single, unconnected `Node` into the graph.

        Parameters
        ----------
        `node` : `Node`
            The `Node` object to add to the graph.
        """
        if node not in self.level.keys():
            self.level[node] = []
            self.node_count += 1
        else:
            raise exceptions.DuplicateNodeException(str(node))

    def random_node(self) -> Node:
        """
        Returns a random `Node`.

        Returns
        -------
        A random `Node`.
        """
        return random.choice(self.nodes())

    def is_junction(self, node: Node) -> bool:
        """
        Checks whether the node is a junction.

        A junction is defined as a node with >1 potential paths where those
        paths are not the path just taken.

        Parameters
        ----------
        `node` : `Node`
            The node to check

        Returns
        -------
        `bool`
            `True` if the `Node` is a junction
        """
        return len(self.level[node]) > 2

    def get_adjacent(self, node: Node) -> list[Node]:
        """
        Returns all nodes adjacent to a given node.

        Parameters
        ----------
        `node` : `Node`
            The node to check

        Returns
        -------
        `list[Node]`
            All adjacent nodes.
        """
        return self.level[node]

    def move_agent(self, old_pos: Position, new_pos: Position, agent: type) -> None:
        """
        Move an agent to the new position.

        It is assumed that the move has already been validated before being passed
        to the graph, as agents should only be able to move a distance of one node
        per move.

        If a collision occurs between an `Agent` and an `Agent` or a `Pickup`, an
        exception will be raised. This is done so that the event can be passed
        back to the `GameManager` so that the collision can be handled here with
        the correct game logic.

        Parameters
        ----------
        `old_pos` : `Position`
            The current position of the agent.
        `new_pos` : `Position`
            The position the agent is moving to.
        `agent` : `type`
            The type of the agent being moved.
        """
        if new_pos == old_pos:
            # If the agent is not moving, nothing should happen
            return
        new_node = self.find_node_by_pos(new_pos)
        old_node = self.find_node_by_pos(old_pos)
        # if passing the above, it is a valid move
        # the move will occur and then it will check if a collision took place
        # which is then raised to be handled by the GameManager
        entity = old_node.get_entity(agent)
        old_node.remove_entity(entity)
        new_node.add_entity(entity)
        if new_node.is_collision():
            # If there is a collision between an agent and a non-empty space,
            # raise exception so that game logic can handle the collision.
            raise exceptions.CollisionException(new_node)

    def find_node_by_pos(self, pos: Position) -> Node:
        """
        Find and return the node at a given position

        Parameters
        ----------
        `pos` : `Position`
            The position to query

        Returns
        -------
        The `Node` with the corresponding position. If none is found then an
        `Exception` is raised.
        """
        for node in self.level.keys():
            if node.position == pos:
                return node
        raise exceptions.NodeNotFoundException(pos)

    def find_node_by_entity(self, entity: Type[Entity]) -> list[Node]:
        """
        Find all `Node` objects matching the type provided.

        Parameters
        ----------
        `entity` : Type[Entity]
            The type of entity to search for.

        Returns
        -------
        A `List` containing all matching `Node` Objects.
        - If `item == Agent`, the list should only contain one value.
        """
        nodes: list[Node] = []
        for node in self.level.keys():
            if node.contains(entity):
                nodes.append(node)
        if len(nodes) == 0:
            raise exceptions.InvalidGraphConfigurationException(
                f"No instances of {entity} could be found."
            )
        return nodes

    def map_edges(self, mapping: dict[Position, list[Position]]) -> None:
        """
        Maps nodes to their adjacent nodes.

        Uses a raw adjacency list to build the internal adjacency list structure,
        converting positions into `Node` objects.

        Parameters
        ----------
        `mapping` : `dict[Position, list[Position]]`
            The raw mapping between nodes and their adjacent nodes.
        """
        for node, children in mapping.items():
            parent = self.find_node_by_pos(node)
            self.level[parent] = []
            for child in children:
                self.level[parent].append(self.find_node_by_pos(child))
        # Manual mapping of portal edges. Assumed that there are only two teleporters
        # and so it is a one-to-one mapping.
        portals = self.find_node_by_entity(Teleporter)
        self.level[portals[0]].append(portals[1])
        self.level[portals[1]].append(portals[0])

        # Check that the graph is connected before returning.
        if not self.is_connected():
            raise exceptions.InvalidGraphConfigurationException(
                "Graph is not connected, check edges"
            )
        self.total_pickups = self.remaining_pickups()

    def bfs(self, start_pos: Position | Node) -> list[Node]:
        """
        Perform a breadth first search on the graph given a starting point.

        Parameters
        ----------
        `start_pos` : `Position | Node`
            The starting point from which to run the search.

        Returns
        -------
        The `list` containing the path of the dfs search.
        """
        start = (
            self.find_node_by_pos(start_pos)
            if isinstance(start_pos, Position)
            else start_pos
        )
        visited: list[Node] = []
        stack: list[Node] = [start]

        while len(stack) > 0:
            current = stack.pop(0)
            visited.append(current)
            for child in self.level[current]:
                if child not in visited and child not in stack:
                    stack.append(child)
        return visited

    def is_connected(self) -> bool:
        """
        Checks that the graph is connected.

        In theory, a graph is fully connected if any `Node` is connected to any
        other node and therefore by selecting a random `Node`, the `bfs` function
        should return a path which contains all `Node` objects within the `Graph`.

        Returns
        -------
        `True` if the `Graph` is connected.
        """
        start: Node = random.choice(list(self.level.keys()))
        path = self.bfs(start)
        return len(path) == len(list(self.level.keys()))

    def is_repeated_cycle(self, path: list[Node]) -> bool:
        """
        Checks whether there is a repeated cycle within the path.

        This is done by checking for two consecutive Nodes being repeated at
        any point within the path.

        Parameters
        ----------
        `path` : `list[Node]`
            The path to check for repetition.

        Returns
        -------
        `True` if there is a repeated cycle.
        """
        for i in range(len(path) - 1):
            pair = [path[i], path[i + 1]]
            for j in range(i + 1, len(path) - 1):
                if [path[j], path[j + 1]] == pair:
                    return True
        return False

    def find_paths_between(self, start_pos: Position, end_pos: Position) -> list[Path]:
        """
        Find all valid paths between two points.

        This function uses a Breadth-First Search algorithm to find all of
        the valid paths between the start and goal nodes. The reason that
        BFS is chosen is that it is the fastest algorithm for finding short
        paths to the goal. Optimal paths are provided early allowing the
        function to be terminated early if the quota for paths (5) has been
        met. An iterative approach was taken over recursion because the graphs
        used for the levels are very complex and therefore could risk a
        RecursionError.

        This function will find and return the five shortest paths. It is up
        to the agents internal decision making to decide which paths are to be
        kept and which are to be pruned. This is because all agents will have a
        different set of criteria for what constitutes a valid path.

        Parameters
        ----------
        `start_pos` : `Position`
            The starting position.
        `end_pos` : `Position`
            The goal position.

        Returns
        -------
        A `list` containing paths of `Node`'s.
        """
        # collect the nodes early so that error raised if they don't exist.
        start_node = self.find_node_by_pos(start_pos)
        end_node = self.find_node_by_pos(end_pos)
        # if the goal node is already found, return
        if start_node == end_node:
            return [Path([start_node])]
        queue = [(start_node, [start_node])]
        paths: list[Path] = []

        while len(queue) > 0:
            current, path = queue.pop(0)
            if current == end_node:
                paths.append(Path(path))
                if len(paths) == 5:
                    # Add breakpoint here once enough paths have been collected
                    break

            for node in self.level[current]:
                if node not in path and not node.contains(Gate):
                    queue.append((node, path + [node]))

        return paths

    def shortest_path_to(self, current: Position, goal: Position) -> Path:
        """
        Finds the shortest path between two nodes,
        irrespective of reward or the presence of ghosts.

        Parameters
        ----------
        `current` : `Position`
            The starting position.
        `goal` : `Position`
            The goal position.

        Returns
        -------
        The shortest `Path`.
        """
        all_paths = self.find_paths_between(current, goal)
        return min(all_paths, key=lambda path: len(path))

    def remaining_pickups(self) -> int:
        """
        Counts the number of pickups remaining on the level.

        Returns
        -------
        The number of non-empty nodes on the graph.
        """
        return sum(node.contains(Pickup) for node in self.nodes())

    def find_path_to_next_jct(self, start_pos: Position) -> list[Path]:
        """
        Find all paths between the current position and the surrounding junctions.

        This function implements a similar BFS algorithm to `find_paths_between`,
        however the goal state in this instance is for the target node to be a
        junction.

        Parameters
        ----------
        `node` : `Node`
            The current position of the agent.

        Returns
        -------
        `Path`
            A path from the current position to the next junction.
        """
        start_node = self.find_node_by_pos(start_pos)
        queue = [(start_node, [start_node])]
        paths: list[Path] = []
        while len(queue) > 0:
            current, path = queue.pop(0)
            if not self.is_junction(current):
                pass

            if not Path(path).is_loop():
                paths.append(Path(path))

            if len(paths) == 10:
                # break when enough paths found
                break
            if len(path) > 12:
                if len(paths) == 0:
                    # raise error if path is too long
                    raise exceptions.PathNotFoundException(start_node.position)
                else:
                    break

            for node in self.level[current]:
                if node not in path and not node.contains(Gate):
                    queue.append((node, path + [node]))
        return paths
