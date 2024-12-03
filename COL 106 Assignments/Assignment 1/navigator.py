from maze import *
from exception import *
from stack import *
class PacMan:
    def __init__(self, grid : Maze) -> None:
        ## DO NOT MODIFY THIS FUNCTION
        self.navigator_maze = grid.grid_representation
    def validmove(self, x, y):
        if(x<0 or x>=len(self.navigator_maze)):
            return False
        if(y<0 or y>=len(self.navigator_maze[0])):
            return False
        if(self.navigator_maze[x][y]==1):
            return False
        return True    
    def find_path(self, start : tuple, end : tuple) -> list:
        # IMPLEMENT FUNCTION HERE
        movelist = [[1,0], [0,1], [-1,0], [0,-1]]
        visited = []
        for x in range(len(self.navigator_maze)):
            vis = []
            for y in range(len(self.navigator_maze[0])):
                vis.append(False)
            visited.append(vis)
        ans = Stack()
        
        if not self.validmove(start[0], start[1]):
            raise PathNotFoundException
        ans.push((start[0], start[1]))
        visited[start[0]][start[1]] = True
        while ans.is_empty() == False:
            
            cur = ans.top()
            # print(cur)
            if(cur[0]==end[0] and cur[1]==end[1]):
                
                 return ans.con_to_list()
            
            found = False
            for i in range(len(movelist)):
                if self.validmove(cur[0]+movelist[i][0], cur[1]+movelist[i][1]) and visited[cur[0]+movelist[i][0]][cur[1]+movelist[i][1]] == False:
                    
                    ans.push((cur[0]+movelist[i][0], cur[1]+movelist[i][1]))
                    visited[cur[0]+movelist[i][0]][cur[1]+movelist[i][1]] = True
                    found = True
                    break
            if found == False:
                ans.pop()
                
                
                
                
        raise PathNotFoundException
